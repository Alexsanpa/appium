Project Settings
================



Default settings
----------------

.. code-block:: ini
	:caption: Default settings
	:name: default_settings

	[ENV]
	DEBUG = false
	CUSTOM_SETTINGS_ENABLED = false
	COMBINE_REPORTS = false
	LOG_FILES_PATH = outputs/logs
	LOG_MAX_DAYS_KEEP = 100
	REPORT_FILES_PATH = outputs/reports
	EXTRA_RESOURCES_PATH = none

	MAIL_SERVER = none
	MAIL_PORT = 587
	MAIL_SSL_PORT = 465
	MAIL_USE_SSL = true

.. code-block:: python
	:caption: Usage in code

	from sapyautomation.core import LazySettings
	
	print(LazySettings().COMBINE_REPORTS)

Custom settings
----------------

.. code-block:: ini
	:caption: Custom settings example
	:name: custom_settings

	[ENV]
	CUSTOM_SETTINGS_ENABLED = True

	[CUSTOM]
	URL_FIORI = http://url

.. code-block:: python
	:caption: Usage in code

	from sapyautomation.core import LazySettings
	
	print(LazySettings().CUSTOM_URL_FIORI)
