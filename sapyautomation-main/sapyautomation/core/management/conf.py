import os
import shutil
from pathlib import Path
from configparser import NoOptionError, ConfigParser, NoSectionError

from sapyautomation.core.utils.strings import TIMESTAMP_FORMAT
from sapyautomation.core.utils.exceptions import (SettingNotFound,
                                                  BadSettings)
from sapyautomation.desktop.files import is_relative_path

DEFAULT_SETTINGS = Path(__file__).parent.joinpath(
    'resources', 'default_settings.ini')

SETTINGS_SECTIONS = ('ENV', 'SAP', 'CUSTOM')


class LazySettings:
    """ Wrapper class to make Settings a unique object(Singleton).

    Attributes:
        instance (`Settings`): instance of Settings class.

    """
    _instance = None

    def __new__(cls, rebuild: bool = False):
        """ Validates if the instance should builded.

        Args:
            rebuild (bool, optional): if True the active _instance will
                be discarted and a new one used instead.

        """
        if rebuild or cls._instance is None:
            cls._instance = Settings()
            cls._instance.configure()

        return cls._instance

    def __getattr__(self, name):
        if hasattr(self._instance, name):
            return getattr(self._instance, name)

        return None


class Settings:
    """ Settings manager class

    Handles the load from default and user-defined settings.

    Note:
        This class shouldn't be called directly, `LazySettings`
        should be called instead.

    """

    def configure(self):
        """ Manages settings from default and user-defined source.

        This class load the default settings and retrieve the user ones
        by the `SAPY_SETTINGS` enviroment parameter.

        If settings file doesn't exists a copy of default_settings would
        be placed.
        """
        self._configured = False

        if not Path(self.SETTINGS_FILE).exists():
            shutil.copy(DEFAULT_SETTINGS, self.SETTINGS_FILE)
        self._loadSettings()
        self._loadSettings()
        self._calculate_path('LOCK_PATH')

    @property
    def TIMESTAMP_FORMAT(self):
        if not hasattr(self, '_TIMESTAMP_FORMAT'):
            self._TIMESTAMP_FORMAT = TIMESTAMP_FORMAT

        return self._TIMESTAMP_FORMAT

    @property
    def SETTINGS_FILE(self):
        if not hasattr(self, '_SETTINGS_FILE'):
            self._SETTINGS_FILE = os.getenv('SAPY_SETTINGS')
        if self._SETTINGS_FILE is None:
            self._SETTINGS_FILE = DEFAULT_SETTINGS

        return self._SETTINGS_FILE

    @property
    def SECRETS_FILE(self):
        if not hasattr(self, '_SECRETS_FILE'):
            self._SECRETS_FILE = self.PROJECT_PATH.joinpath('secrets.ini')

        return self._SECRETS_FILE

    @property
    def PROJECT_PATH(self):
        if not hasattr(self, '_PROJECT_PATH'):
            self._PROJECT_PATH = Path(self.SETTINGS_FILE).parent

        return self._PROJECT_PATH

    def _calculate_path(self, attr_name: str):
        """ Calculate absolute path
        """
        attr = getattr(self, attr_name)
        if is_relative_path(attr):
            attr = self.PROJECT_PATH.joinpath(attr)
        else:
            attr = Path(attr)

        setattr(self, attr_name, attr)

    def CREDENTIALS(self, name):
        """ Returns credentials by section name

        Args:
            name: section name in secrets.ini

        """
        if not hasattr(self, '_CREDENTIALS'):
            self._loadCredentials()

        return self._CREDENTIALS[name]

    def _loadCredentials(self):
        """ Load credentials from secrets file.

        This class load the secrets file specified by `path` and
        converts the values into credentials for easy use.

        """

        secrets = ConfigParser()
        secrets.read(self.SECRETS_FILE)
        self._CREDENTIALS = {}

        for section in secrets.sections():
            section = section.upper()
            self._CREDENTIALS[section] = {}

            for key in secrets[section].keys():
                key = key.upper()
                self._CREDENTIALS[section][key] = secrets[section][key]

    def _loadSettings(self):
        """ Converts settings files into attributes.

        This class load the settings file specified by `path` and
        converts the values into attributes for easy use.

        if `self._configured` is False this class loads the default settings.
        """

        settings = ConfigParser()

        if self._configured:
            settings.read(self.SETTINGS_FILE)
        else:
            settings.read(DEFAULT_SETTINGS)

        try:
            custom_settings = settings.get('ENV',
                                           'CUSTOM_SETTINGS_ENABLED')
            custom_settings = bool(custom_settings.lower() == 'true')
        except NoSectionError:
            raise BadSettings("Missing 'ENV' section.")
        except NoOptionError:
            raise BadSettings("Setting 'CUSTOM_SETTINGS_ENABLED'"
                              "is required as minimum setup.")

        for section in settings.sections():
            section = section.upper()
            for key in settings[section].keys():
                key = key.upper()
                if section == 'ENV' and key.split('_')[0] in SETTINGS_SECTIONS\
                        and key != 'CUSTOM_SETTINGS_ENABLED':
                    raise BadSettings("'%s' tries to override '%s' section, "
                                      "define the key inside the section"
                                      % (key, key.split('_')[0]))
                setting = settings[section].get(key, '__empty__')
                setting = self._parse_specials(setting)

                if setting != '__empty__':
                    if section != 'ENV':
                        key = '%s_%s' % (section, key)

                    if self._configured and not hasattr(self, key):
                        if section == 'CUSTOM' and not custom_settings:
                            raise SettingNotFound(
                                "Custom settings are not enabled.")
                        if section != 'CUSTOM':
                            raise SettingNotFound(
                                "'%s' is not a valid setting" % key)

                    setattr(self, key, setting)

        self._configured = True

    @staticmethod
    def _parse_specials(value):
        """ Tries to parse value as boolean, if can't just returns
        the original value
        Args:
            value: value to be parsed as boolean
        """
        new_value = value.lower()
        if new_value == 'false':
            value = False
        elif new_value == 'true':
            value = True
        elif new_value == 'none':
            value = None

        return value
