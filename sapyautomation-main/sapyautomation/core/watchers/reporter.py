import shutil
import importlib
from datetime import datetime, timedelta
from pathlib import Path
from logging import INFO, DEBUG, WARNING, ERROR
from fpdf.fpdf import FPDF

try:
    from pdf2docx import parse  # pylint: disable=import-error
except ModuleNotFoundError:
    pass

from sapyautomation.core.management.conf import LazySettings
from sapyautomation.core.watchers.logger import Logger
from sapyautomation.core.utils.strings import string_to_pep_convention,\
    wrap_text, convert_text_to_matrix
from sapyautomation.core.utils.general import (get_source_lines, get_resource,
                                               PackedData)
from sapyautomation.desktop.files import path_to_module,\
    generate_unique_filename, ConfigFile, merge_pdfs
from sapyautomation.core.utils.exceptions import EvidenceOutOfStep


class LazyReporter:
    """ Wrapper class to make reporter a unique object(Singleton).

    Attributes:
        instance (:obj: `Settings`): instance of Reporter class.
    """

    _instance = None

    def __new__(cls, name: str = None, rebuild: bool = False):
        """ Validates if the instance should builded.

        Args:
            name (str): reporter name.
            rebuild (bool, optional): if True the active _instance will
                be discarted and a new one used instead.

        Returns:
            The actual Reporter instance or creates a new one.
        """

        if rebuild or cls._instance is None:
            cls._instance = Reporter()
            cls._instance.generate_paths()
        if name is not None:
            cls._instance.configure(name)

        return cls._instance

    def __getattr__(self, name):
        if hasattr(self._instance, name):
            return getattr(self._instance, name)

        return None


class Reporter:
    """ Reporting manager class

    Handles the collect and formating for report's data.

    Attributes:
        _registry(`dict`): Collection of tests instances for
            report's data.
        _data(`dict`): Collection of tests data for report.

    Note:
        This class shouldn't be called directly, `LazyReporter`
        should be called instead.
    """
    def __init__(self):
        self.__evidences = {}
        self.__logger = {}
        self.__registry = {}
        self.__evidence_report = {}
        self.paths = {}

    @property
    def uid(self):
        """ returns te unique identifier for the actual execution """
        return self.paths['logger_path'].parts[-1]

    def generate_paths(self):
        """ Generates path with unique identifier for actual execution """

        uid = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = Path(LazySettings().PROJECT_PATH)

        logger_path = path.joinpath(LazySettings().LOG_FILES_PATH, uid)
        report_path = path.joinpath(LazySettings().REPORT_FILES_PATH)
        evidence_path = report_path.joinpath('evidence', uid)
        evidence_report_path = report_path.joinpath('docs')

        report_path.joinpath('video').mkdir(parents=True, exist_ok=True)
        logger_path.mkdir(parents=True, exist_ok=True)
        evidence_path.mkdir(parents=True, exist_ok=True)
        evidence_report_path.mkdir(parents=True, exist_ok=True)
        LazySettings().LOCK_PATH.mkdir(parents=True, exist_ok=True)

        resource = report_path.joinpath('bootstrap.min.css')
        if not resource.exists():
            shutil.copy(str(get_resource('reports/bootstrap.min.css')),
                        str(resource))

        resource = report_path.joinpath('jquery.min.js')
        if not resource.exists():
            shutil.copy(str(get_resource('reports/jquery.min.js')),
                        str(resource))

        self.paths['logger_path'] = logger_path
        self.paths['report_path'] = report_path
        self.paths['evidence_path'] = evidence_path
        self.paths['evidence_report_path'] = evidence_report_path

    def configure(self, name: str):
        """ Initializes the reporter instance. """
        self.__debug = LazySettings().DEBUG
        self.__name = name

        self.add_registry_data('tests', self.__name)

        if self.__name not in self.__evidences.keys():
            self.__evidences[self.__name] = []

        if self.__name not in self.__logger.keys():
            self.__logger[self.__name] = Logger(self.__name,
                                                self.paths['logger_path'])

        if self.__name not in self.__evidence_report.keys():
            self.__evidence_report[self.__name] = []

    def _reporter_debug(self, msg):
        self.add_to_log("Reporter%s" % msg)

    @property
    def data(self):
        """ Dynamic loader for data dict """
        if not hasattr(self, '_data'):
            self._data = {}

        return self._data

    @property
    def _registry(self) -> dict:
        """ Dynamic loader for registry dict """
        if not hasattr(self, '__registry'):
            self.__registry = {}

        return self.__registry

    @property
    def _debug(self) -> bool:
        """ Dynamic loader for debug flag """
        if not hasattr(self, '__debug'):
            self.__debug = False

        return self.__debug

    def add_test_data(self, key: str, test_method: str, value=None):
        """ Saves data to the `data` property.

        Args:
            key (`str`): Parent TestCase Class's name.
            test_method (`str`): Case method's name.
            value: Extra data.
        """
        if value is None and key not in self.data.keys():
            self.data[key] = []

        elif key in self._data.keys():
            self.data[key].append((test_method, value))

        elif key not in self._data.keys():
            self.data[key] = [(test_method, value), ]

        self._reporter_debug("(data)key: %s, test_method:%s, value:%s" % (
            key, test_method, value))

    def registry_keys(self):
        """ Dynamic load of resgistry key elements """

        return self._registry.keys()

    def get_registry_data(self, key: str):
        """ Returns registry data
        Args:
            key: This is what we are looking for
        """
        if key not in self.registry_keys():
            return None

        return self.__registry[key]

    def add_registry_data(self, key: str, value=None):
        """ Saves data to the `registry` property.

        Args:
            key (`str`): Parent TestCase Class's name.
            value: TestCase instance.
        """
        if key in self.registry_keys() and value is not None:
            self.__registry[key].append(value)
        elif key in self.registry_keys() and value is None:
            self.__registry[key] = []
        elif key in self.registry_keys() and value is not None:
            self.__registry[key] = [value, ]

    def get_test_data(self, test_case_class: str = None) -> dict:
        """ Gets necessary data for report generation

        Args:
            test_case_class (str): Parent TestCase Class's name.

        Returns:
            A dict with the tracking data necessary for reports.

        """

        if test_case_class is None:
            return self.__registry

        return self.__registry[test_case_class]

    # -------- LOGGER ------- #

    @property
    def _logger(self) -> Logger:
        """ Dynamic loader for logger instance """

        return self.__logger[self.__name]

    @property
    def logger_entries(self) -> list:
        """ Returns an array of active logger entries
        """
        logger_path = self.__logger[self.__name].file_path('debug')
        entries = None

        with logger_path.open() as lf:
            entries = lf.readlines()

        return entries

    def add_to_log(self, msg: str, level: str = DEBUG, log_at: str = None):
        """ Adds an entry to logger
        Args:
            msg(str): message to be logged.
            level(str): logging level of the message.
        """
        if level is DEBUG:
            self._logger.debug(msg)
        elif level is INFO:
            self._logger.info(msg)
        elif level is WARNING:
            self._logger.warning(msg)
        elif level is ERROR:
            self._logger.error(msg, log_at)

    # ------ EVIDENCES ------ #

    @property
    def evidences(self):
        """ returns evidences for configured test suite
        """
        return self.__evidences[self.__name]

    def start_record(self, suite_name: str, case_name: str,
                     extra_uid: int = 0):
        """ Starts evidence recording

        Args:
            suite_name(str): name of the test case module.
            case_name(str): name of the test case class.
            extra_uid(int): extra uid for multiple execs identification.

        """
        if LazySettings().TEST_RECORDING_ENABLED:
            from sapyautomation.desktop.screen import ScreenCapture

            path = self.paths['report_path'].joinpath(
                'video', self.uid, '00_%s_%s-%s.avi' % (suite_name,
                                                        case_name, extra_uid))
            path = generate_unique_filename(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path = '/'.join([LazySettings().REPORT_FILES_PATH, 'video',
                             path.parts[-2], path.parts[-1]])

            self.__recorder = ScreenCapture()
            self.__recorder.start_record(path, 15)

            self.__evidences[suite_name].append(Path(path).parts[-1])

            return path

        return None

    def stop_record(self):
        """ Stops evidence recording
        """
        if LazySettings().TEST_RECORDING_ENABLED:
            self.__recorder.stop_record()

            return self.__recorder.record_data()

        return None

    def save_evidence(self, suite_name: str, case_name: str,
                      await_before: float = 0.1, await_after: float = 0.1,
                      extra_uid: int = 0, asynchronous: bool = False):
        """ Saves a screenshot as evidence

        Args:
            suite_name(str): test module name.
            case_name(str): test name.
            await_before(float): seconds to await before taking evidence
            await_after(float): seconds to await after taking evidence
            extra_uid(int): Execution index for evidence tagging
            on multiple test execution.
            asynchronous(bool): Flag to take screenshot asynchronously.

        Returns:
            evidence file path
        """
        from sapyautomation.desktop.screen import ScreenCapture

        path = self.paths['evidence_path'].joinpath(
            '00_%s_%s-%s.png' % (suite_name, case_name, extra_uid))
        path = generate_unique_filename(path)
        ScreenCapture().take_screenshoot(path, await_before, await_after,
                                         asynchronous)

        self.__evidences[suite_name].append(path.parts[-1])
        return path

    # ------ REPORTS ------ #

    @property
    def evidence_report(self):
        """  Retrieves actual evidence report
        """

        return self.__evidence_report[self.__name]

    def case_report(self, case):
        """ Collects data required to report
        Args:
            case: testcase object
        """
        data = {
                'sapy_cases_source': {
                    case._testMethodName: get_source_lines(case)},
                'sapy_cases_log': {
                    self.__name: self._logger.file_path(is_relative=True)},
                'sapy_cases_evidence': {self.__name: self.evidences},
                'sapy_resumed_from': {self.__name: case.resumed_test},
                'sapy_cases_evidence_report': {
                    self.__name: self.evidence_report}}
        return data

    @staticmethod
    def _execution_history(test_class: str = None,
                           only_not_reported: bool = False):
        """ Returns lock files as an test executions history array

        Args:
            test_class(str): Test class name of wanted history.
                leave as None if want all tests history.
            only_not_reported(bool): Set 'True' if want to get
                only non reported history
        """
        executions = []
        if test_class is None:
            lock_files = LazySettings().LOCK_PATH.glob('.*')
        else:
            lock_files = LazySettings().LOCK_PATH.glob('.*_%s' % test_class)

        for item in lock_files:
            if item.is_file():
                lock = PackedData(item.parts[-1][1:], auto_save=True)
                reported = lock.get('reported')

                if only_not_reported and not reported or not only_not_reported:
                    executions.append(lock)

        return executions

    def execution_report(self, keys: list, test_classes: list = None,
                         ignore_repeated: bool = True):
        """ Retrieves data from executed tests

        Note:
            if test_classes is None test nmaes will be recovered from loggers

        Args:
            keys(list): list of key names from lock file
            test_clases(list): list of tests class-name to be reported
            ignore_repeated(bool): flag to ignore duplicates
        """
        execution = []
        tests = test_classes if test_classes is not None \
            else [t for t in self.__logger if 'sapyautomation' not in t]

        if ignore_repeated:
            new_tests = []
            for test in tests:
                if test not in new_tests:
                    new_tests.append(test)
            tests = new_tests

        for test in tests:
            pdata = self._execution_history(test)[-1]
            pdata.replace_or_append('reported', True)

            if pdata.key_exists('_3pa_data'):
                report_data = pdata.get('_3pa_data')
            else:
                report_data = {}

            for key in [k for k in keys if pdata.key_exists(k)]:
                report_data[key] = pdata.get(key)

            report_data['data'] = []
            for key in [k for k in pdata.keys()
                        if k not in keys + ['status', 'steps',
                                            'target_datetime',
                                            'pauses', '_3pa_data']]:
                report_data['data'].append('%s=%s' % (key, pdata.get(key)))

            execution.append(report_data)

        return execution

    def evidences_report(self, test_class):
        """ Generates report data for pdf report.

        Args:
            test_class(obj): Test class object.

        """
        steps = {}
        actual_step = None
        for entry in self.logger_entries:
            if 'Step' in entry and 'Step skipped' not in entry:
                actual_step = entry.split(']')[1].strip()
                if actual_step not in steps.keys():
                    steps[actual_step] = ['', [], []]

            elif 'Evidence:' in entry:
                # TODO: leave exception or report message pylint: disable=fixme
                if actual_step is None and "screenshot saved" in entry:
                    raise EvidenceOutOfStep()

                label = entry.split("|")[-1]
                for evidence in [fragment for fragment in entry.split("'")
                                 if '.png' in fragment]:
                    steps[actual_step][1].append((evidence, label))
            elif "Label:" in entry:
                label = entry.split("|")[-1]
                steps[actual_step][2].append(label)

        for step in steps:
            method_name = string_to_pep_convention(step.replace(':', ''))
            method = getattr(test_class, method_name)
            steps[step][0] = method.__doc__

        return steps

    def save_evidence_report(self, suite: str = None, errors=None,
                             test_duration=None):
        """ Generates pdf report.

        Args:
            suite(str): path to test module.
            errors: list of errors.

        """
        report_language = LazySettings().REPORT_LANGUAGE
        table_location = LazySettings().REPORT_TABLE_LOCATION

        if report_language == "ESP":
            TABLE_DATA = [
                ["Paso", "Descripción", "Resultado esperado", "Estatus"]
            ]
        elif report_language == "POR":
            TABLE_DATA = [
                ["Passo", "Descrição", "Resultado esperado", "Status"]
            ]
        else:
            TABLE_DATA = [
                ["Step", "Description", "Expected result", "Status"]
            ]
        step_counter = 1

        name = f"{self.uid}_{self.__name}"
        lockfile = PackedData(name)
        report_path = generate_unique_filename(
            self.paths['evidence_report_path'].joinpath(
                f"{name}.docx" if LazySettings().REPORT_DOCX_FORMAT
                else f"{name}.pdf"))
        report_file = report_path.parts[-1]
        if '.docx' in report_file:
            report_path = report_path.parent.joinpath(
                f"{report_file[:-4]}pdf")

        report_path = self.paths['evidence_report_path'].joinpath(report_path)

        if suite is not None:
            test_module = importlib.import_module(path_to_module(suite))
            test_class = getattr(test_module, self.__name)
            test_name = path_to_module(suite).split('.')[-1]
            test_name = ' '.join(test_name.split('_')[1:]).title()

            data = self.evidences_report(test_class)

            pdf = PDFReport(report_path)
            pdf.add_page()
            first_page = True
            test_case_language = "Test case: %s"
            if report_language == "ESP":
                test_case_language = "Caso de prueba: %s"
            elif report_language == "POR":
                test_case_language = "Caso de teste: %s"
            
            for step in data:
                """Extracts TABLE_DATA from steps"""
                if data[step][0] is not None:
                    table_row = [str(step_counter)]
                    desc_and_expected = data[step][0].split('\n')
                    desc_and_expected = [ele for ele in desc_and_expected if ele.strip()]

                    description = desc_and_expected[0].strip()
                    expected_result = desc_and_expected[1].strip()

                    desc_index = description.find(':')
                    expected_index = expected_result.find(':')

                    table_row.append(description[desc_index+1:].strip())
                    table_row.append(expected_result[expected_index+1:].strip())

                    lockfile.readFromFile()
                    pep_step = string_to_pep_convention(step)
                    if lockfile.get('status') == 'failed' \
                            and lockfile.get('failure') == pep_step:
                        table_row.append('Failed')
                        TABLE_DATA.append(table_row)
                        break
                    step_counter += 1
                    table_row.append('Passed')
                    TABLE_DATA.append(table_row)

                
            for step in data:
                pdf.set_font('Helvetica', '', 20)
                if first_page:
                    
                    lockfile.readFromFile()
                    test_name_docstring = lockfile.get('test_name')

                    title = test_class.__doc__ \
                        if LazySettings().REPORT_DOC_TITLE \
                        else test_case_language % test_name_docstring
                    title = test_case_language % test_name_docstring \
                        if title is None else title.strip()

                    for wrapped_line in wrap_text(title, 58):
                        pdf.cell(0, 10, wrapped_line)
                        pdf.ln(6)

                    pdf.ln(15)
                    pdf.set_font('Helvetica', 'I', 12)
                    test_duration = float(test_duration[:-1])
                    test_duration = timedelta(seconds=test_duration)
                    if report_language == "ESP":
                        pdf.cell(0, 10, f"Duración: {test_duration}".split('.')[0])
                    elif report_language == "POR":
                        pdf.cell(0, 10, f"Duração: {test_duration}".split('.')[0])
                    else:
                        pdf.cell(0, 10, f"Duration: {test_duration}".split('.')[0])
                    pdf.ln(5)
                    pdf.cell(0, 10, "_________________________________________"
                             "_______________________________________")
                    pdf.ln(10)
                    if table_location == "top":
                        # CREATE TABLE
                        pdf.set_font('Helvetica', '', 12)
                        with pdf.table(col_widths=(9,53,53,14), text_align=("CENTER", "LEFT", "LEFT", "CENTER")) as table:
                            for data_row in TABLE_DATA:
                                row = table.row()
                                for datum in data_row:
                                    row.cell(datum)
                    first_page = False

                # Step name
                pdf.set_font('Helvetica', '', 20)
                pdf.ln(8)

                for wrapped_line in wrap_text(step, 58):

                    if report_language == "ESP":
                        new_wrapped_line = wrapped_line.replace("Step", "Paso")
                    elif report_language == "POR":
                        new_wrapped_line = wrapped_line.replace("Step", "Passo")
                    else:
                        new_wrapped_line = wrapped_line

                    pdf.cell(0, 10, new_wrapped_line)
                    pdf.ln(6)

                # Docstring
                pdf.set_font('Helvetica', 'I', 14)
                step_table = []
                if data[step][0] is not None:
                    step_table = convert_text_to_matrix(data[step][0])
                    # step_details = data[step][0].split('\n')
                    # for ele in step_details:
                    #     if ele.strip():
                    #         step_table.append([ele.strip()])
                pdf.ln(3)
                pdf.set_line_width(.5)
                with pdf.table(first_row_as_headings=False, col_widths=(22, 100), text_align=("LEFT", "LEFT"), line_height=6) as table:
                    for data_row in step_table:
                        row = table.row()
                        for datum in data_row:
                            row.cell(datum)
                pdf.ln(4)
                for evidence in data[step][1]:
                    pdf.image(evidence[0], w=pdf.w*0.9)
                    pdf.ln(3)
                    for wrapped_line in wrap_text(evidence[1]):
                        pdf.cell(0, 5, f"{wrapped_line}", align="R", ln=1)

                    pdf.ln(3)
                # Added text/label to PDF report from add_label() method
                for evidence in data[step][2]:
                    # Line break 5p from last cell
                    pdf.ln(1)
                    # Output justified text
                    pdf.multi_cell(0, 2, f"{evidence}")

                lockfile.readFromFile()
                pep_step = string_to_pep_convention(step)
                if lockfile.get('status') == 'failed' \
                        and lockfile.get('failure') == pep_step:
                    break

            if errors is not None and len(errors) > 0:
                pdf.add_page()
                pdf.set_font('Helvetica', '', 12)
                for error in errors:
                    for line in error.split('\n'):
                        for w_line in wrap_text(line, 100):
                            pdf.cell(0, 10, w_line)
                            pdf.ln(5)
            
            if table_location == "bottom":
                # CREATE TABLE
                pdf.add_page()
                pdf.set_font('Helvetica', '', 12)
                with pdf.table(col_widths=(9,53,53,14), text_align=("CENTER", "LEFT", "LEFT", "CENTER")) as table:
                    for data_row in TABLE_DATA:
                        row = table.row()
                        for datum in data_row:
                            row.cell(datum)
            pdf.save()

        self.__evidence_report[self.__name].append(report_file)


class PDFReport(FPDF):
    """ PDF report generation class
    """
    def __init__(self, path: str, orientation='P', unit='mm',
                 page_format='A4'):
        self.__path = path
        res_path = Path(LazySettings().PROJECT_PATH).joinpath('resources',
                                                              'reports')
        self.__data = ConfigFile(res_path.joinpath("pdf_data.ini"),
                                 get_resource("reports/pdf_data_template.ini"))
        super().__init__(orientation, unit, page_format)

    def header(self):
        """ Page's header
        """
        report_language = LazySettings().REPORT_LANGUAGE
        if report_language == "ESP":
            page_number_text = f"Página {self.page_no()}"
        elif report_language == "POR":
            page_number_text = f"Página {self.page_no()}"
        else:
            page_number_text = f"Page {self.page_no()}"
        filename = self.__path.parts[-1] \
            if(self.__data.get_bool('HEADER', 'SHOW_FILE_NAME')) else ""
        page_number = page_number_text \
            if(self.__data.get_bool('HEADER', 'SHOW_PAGE_NUMBER')) else ""
        timestamp = self.datetime \
            if(self.__data.get_bool('HEADER', 'SHOW_DATE')) else ""
        text = self.__data.get_str('HEADER', 'TEXT')

        self.set_text_color(31, 73, 125)
        self.set_font('Helvetica', 'I', 10)
        self.cell(self.w*0.3, 0, filename, 0, 0, 'L')
        self.cell(0, 0, page_number, 0, 0, 'R')
        self.cell(self.w*-0.6)
        self.cell(self.w*0.3, 7, timestamp, 0, 0, 'C')
        self.set_font('Helvetica', 'B', 12)
        self.cell(self.w*-0.3)
        self.cell(self.w*0.3, 15, "" if text is None else text, 0, 0, 'C')
        self.cell(self.w*-0.6, 20)
        if(self.__data.get_bool('HEADER', 'SHOW_LOGO_A')):
            try:
                self.image(get_resource('reports/logo_a.jpg'), h=5, y=13)

            except FileExistsError as e:
                self.image(get_resource('reports/missing_logo.jpg'), h=5, y=13)
                print(e)

        if(self.__data.get_bool('HEADER', 'SHOW_LOGO_B')):
            try:
                self.image(get_resource('reports/logo_b.jpg'),
                           h=5, x=self.w*0.75, y=13)

            except FileExistsError as e:
                self.image(get_resource('reports/missing_logo.jpg'),
                           h=5, x=self.w*0.75, y=13)
                print(e)

        self.set_line_width(0.3)
        self.set_draw_color(31, 73, 125)
        self.line(10, 22, self.w-10, 22)
        self.ln(20)

    def footer(self):
        """ Page's footer
        """
        report_language = LazySettings().REPORT_LANGUAGE
        if report_language == "ESP":
            page_number_text = f"Página {self.page_no()}"
        elif report_language == "POR":
            page_number_text = f"Página {self.page_no()}"
        else:
            page_number_text = f"Page {self.page_no()}"

        filename = self.__path.parts[-1] \
            if(self.__data.get_bool('FOOTER', 'SHOW_FILE_NAME')) else ""
        page_number = page_number_text \
            if(self.__data.get_bool('FOOTER', 'SHOW_PAGE_NUMBER')) else ""
        timestamp = self.datetime \
            if(self.__data.get_bool('FOOTER', 'SHOW_DATE')) else ""
        text = self.__data.get_str('FOOTER', 'TEXT')

        self.set_y(-20)
        self.set_text_color(31, 73, 125)
        self.set_font('Helvetica', 'B', 10)
        self.cell(self.w*0.3, 10, "" if text is None else text,
                  0, 0, 'L')

        self.set_font('Helvetica', 'I', 10)
        self.cell(self.w*-0.3)
        self.cell(self.w*0.3, 25, timestamp, 0, 0, 'L')

        self.set_font('Helvetica', 'B', 10)
        self.cell(0, 10, page_number, 0, 0, 'R')
        filename = filename.replace('.pdf', '')
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 25, filename, 0, 0, 'R')

        if(self.__data.get_bool('FOOTER', 'SHOW_LOGO_A')):
            try:
                self.image(get_resource('reports/logo_a.jpg'),
                           h=5, x=self.w*0.35, y=self.h-17)

            except FileExistsError as e:
                self.image(get_resource('reports/missing_logo.jpg'),
                           h=5, x=self.w*0.35, y=self.h-17)
                print(e)

        if(self.__data.get_bool('FOOTER', 'SHOW_LOGO_B')):
            try:
                self.image(get_resource('reports/logo_b.jpg'),
                           h=5, x=self.w*0.55, y=self.h-17)

            except FileExistsError as e:
                self.image(get_resource('reports/missing_logo.jpg'),
                           h=5, x=self.w*0.55, y=self.h-17)
                print(e)

        self.set_line_width(0.3)
        self.set_draw_color(31, 73, 125)
        self.line(10, self.h-20, self.w-10, self.h-20)

    @property
    def filename(self):
        return self.__path.parts[-1]

    @property
    def datetime(self):
        parts = self.filename.split("_")
        return f"{parts[0].replace('-', '/')} {parts[1].replace('-', ':')}"

    def save(self):
        cover_name = self.__data.get_str('TEMPLATE', 'COVER_FILE')
        report_file = str(self.__path.absolute())
        self.output(self.__path, 'F')
        if cover_name is not None:
            cover_file = str(get_resource(f"reports/{cover_name}.pdf"))

            merge_pdfs((cover_file, report_file),
                       report_file)

        if LazySettings().REPORT_DOCX_FORMAT:
            docx_path = self.__path.parent.joinpath(
                f"{self.filename[:-3]}docx")
            parse(report_file, docx_path, start=0)
            #self.__path.unlink()
