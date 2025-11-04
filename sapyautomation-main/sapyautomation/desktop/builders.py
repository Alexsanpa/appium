from pathlib import Path

from sapyautomation.core.utils.general import get_resource
from sapyautomation.core.utils.strings import string_to_pep_convention,\
    Convention


class TestBuilder:
    def __init__(self, module_name, module_doc, class_doc):
        class_name = string_to_pep_convention(
            module_name, Convention.camel_case).title()

        resource_path = Path(get_resource('tests/test_template.txt'))
        self.module_code = []
        self.steps = []
        self.steps_code = []
        with resource_path.open() as template:
            for line in template.readlines():
                if '$CLASS_NAME$' in line:
                    parts = line.split('$CLASS_NAME$')
                    line = ''.join((parts[0], class_name, parts[1]))

                if '$MODULE_DOC$' in line:
                    parts = line.split('$MODULE_DOC$')
                    line = '%s%s%s' % (parts[0],
                                       '\n'.join(module_doc),
                                       parts[1])

                if '$CLASS_DOC$' in line:
                    parts = line.split('$CLASS_DOC$')
                    line = '%s%s %s' % (parts[0],
                                        '\n'.join(class_doc),
                                        parts[1])

                if '$TEST_METHOD_NAME$' in line:
                    parts = line.split('$TEST_METHOD_NAME$')
                    line = ''.join((parts[0], module_name, parts[1]))

                self.module_code.append(line)

    def add_method(self, method_name, docstring):
        resource_path = Path(get_resource('tests/step_template.txt'))
        self.steps_code.append('\n\n')
        self.steps.append('        self.%s()\n' % method_name)
        with resource_path.open() as template:
            for line in template.readlines():
                if '$STEP_NAME$' in line:
                    parts = line.split('$STEP_NAME$')
                    line = ''.join((parts[0], method_name, parts[1]))

                if '$STEP_DOC$' in line:
                    parts = line.split('$STEP_DOC$')
                    line = '%s%s%s' % (
                        parts[0], '\n        '.join(docstring),
                        parts[1])

                self.steps_code.append(line)

    def save(self, module_path):
        if module_path.exists():
            return "'%s/%s' already exists." % (module_path.parts[-2],
                                                module_path.parts[-1])

        module_path.parent.mkdir(parents=True, exist_ok=True)
        new_lines = []
        for i, line in enumerate(self.module_code):
            if '$STEPS_CALLS$' in line:
                new_lines = self.module_code[:i]
                new_lines = new_lines + self.steps
                self.module_code = new_lines + self.module_code[i+1:]

        for i, line in enumerate(self.module_code):
            if '$STEPS_METHODS$' in line:
                new_lines = self.module_code[:i-1]
                new_lines = new_lines + self.steps_code
                self.module_code = new_lines + self.module_code[i+1:]

        with module_path.open('w+') as module:
            module.writelines(self.module_code)

        return "'%s/%s' created." % (module_path.parts[-2],
                                     module_path.parts[-1])
