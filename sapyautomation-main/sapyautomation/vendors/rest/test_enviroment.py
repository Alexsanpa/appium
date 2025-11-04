import os
from sapyautomation.core.test_cases.bases import BaseTestCases, BasePom
from sapyautomation.web.api_utils import RequestConstructor
from sapyautomation.vendors.rest.models import RequestType


class RestTestSuite(BaseTestCases):
    """Rest API test suite is used as parent class for the test cases

    In this class we created the basic methods to make API testing scripts
    easily adding methods and custom asserts.
    """
    __parameters = {}
    __base_url = None

    def __init__(self, methodName='runTest', ignore_steps=None,
                 resumed_test=None, data_file=None, exec_id=None):
        super().__init__(methodName, ignore_steps, resumed_test, data_file,
                         exec_id)
        self.__pom = RestBasePom()

    def get_env_data(self, *env_names):
        """ Validates enviroment variables and creates a data dict

        Args:
            *args: enviroment variables names
        """
        self.data = {}
        missing_vars = []

        for item in env_names:
            try:
                self.data[item] = os.environ[item]
            except KeyError as e:
                missing_vars.append(str(e)[1:-1])

        if len(missing_vars) > 0:
            raise Exception(f"Missing enviroment variables: {missing_vars}")

    def log(self, msg: str):
        """ This add a DEBUG message to the logger

        Args:
            msg(str): the message to be added.
        """
        self.__pom.log(msg)

    def log_error(self, msg: str):
        """ This add an ERROR message to the logger

        Args:
            msg(str): the message to be added.
        """
        self.__pom.log_error(msg)

    def add_api_parameter(self, key: str, value: str):
        """ Adds or replaces general parameters to be use in API requests.

        Note:
            The parameters defined with this method will be used on all
            requests.

        Args:
            key(str): parameter key to be used in API request.
            value(str): parameter's value.
        """
        self.__parameters[key] = value

    def rm_api_parameter(self, key: str):
        """ Removes a parameter from general parameters.

        Args:
            key(str): parameter key to be removed.
        """
        self.__parameters.popitem(key, None)

    def on_resume(self):
        """ Setting up for test case resumming
        """

    def assertKeyInResponse(self, response: object, key: str) -> None:
        """ Assert to validate that a certain key exists in response

        Args:
            response(obj): the response object.
            key(str): key name
        """
        if key not in response.json():
            self.log_error(f"Assert False: key '{key}' not found in response")
            raise self.failureException(f"Key '{key}' not found in response")

        self.log(f"Assert True: key '{key}' found in response")
        return True

    def assertKeyNotInResponse(self, response, key: str) -> None:
        """ Assert to validate that a certain key don't exists in response

        Args:
            response(obj): the response object.
            key(str): key name
        """
        if key in response.json():
            self.log_error(f"Assert False: key '{key}' found in response")
            raise self.failureException(f"Key '{key}' found in response")

        self.log(f"Assert True: key '{key}' not found in response")
        return True

    def assertKeyValue(self, response, key: str, value: str) -> None:
        """ Assert to validate that a certain key in response
        has an specific value.

        Args:
            response(obj): the response object.
            key(str): key name
            value(str): key value
        """
        if response.json()[key] != value:
            self.log_error(f"Assert False: '{key}' has not "
                           f"'{response.json()[key]}' value.")
            raise self.failureException(f"'{key}' has not "
                                        f"'{response.json()[key]}' value.")

        self.log(f"Assert True: '{key}' has '{response.json()[key]}' value")
        return True

    def assertIsResponseStatus(self, response, status_code: int) -> None:
        """ Assert to validate a specific status code is in response

        Args:
            response(obj): the response object.
            status_code(str): status code to validate.
        """
        if response.status_code != status_code:
            self.log_error(f"Assert False: response has code "
                           f"'{response.status_code}', '{status_code}' "
                           "was expected")
            raise self.failureException("Response has code "
                                        f"'{response.status_code}', "
                                        f"'{status_code}' was expected")

        self.log(f"Assert True: response has code '{response.status_code}'")
        return True

    def assertIsNotResponseStatus(self, response, status_code: int) -> None:
        """ Assert to validate a specific status code is not in response

        Args:
            response(obj): the response object.
            status_code(str): status code to validate.
        """
        if response.status_code == status_code:
            self.log_error("Assert False: response has code "
                           f"'{response.status_code}'")
            raise self.failureException(
                f"Response '{response.status_code}' was not expected")

        self.log("Assert True: response has not code "
                 f"'{response.status_code}'")
        return True


class RestBasePom(BasePom):
    """ Base Rest API POM
    """
    base_url = None

    def _post(self, path: str, headers: dict, params: dict):
        """ Method to make a POST request to the base url

        Args:
            path(str): url path for the call
            header(dict): header parameters for the call
            params(dict): data parameters for the call
        """
        request = RequestConstructor(self.base_url, path, headers, params,
                                     RequestType.POST)
        self.log(f"Request url: {request.request.url}")
        self.__log_parameters(params)
        return request.execute()

    def _get(self, path: str, headers: dict, params: dict):
        """ Method to make a GET request to the base url

        Args:
            path(str): url path for the call
            header(dict): header parameters for the call
            params(dict): data parameters for the call
        """
        request = RequestConstructor(self.base_url, path, headers, params,
                                     RequestType.GET)
        self.log(f"Request url: {request.request.url}")
        self.__log_parameters(params)
        return request.execute()

    def __log_parameters(self, data: dict):
        """ This method add the given data parameters to the logger.
        Args:
            data(dict): data parameters to be added.
        """
        self.log("Parameters sent...")
        for key in data.keys():
            self.log(f"{key} = {data[key]}")

        self.log("")
