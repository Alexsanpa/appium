Case Construction
=================

For the test case's construction we need to understand a few concepts:

Settings
--------

For the framework to work properly we need to create a **settings.ini** file at project root.
The keys defined in our settings file can be accessed by the LazySettings object.
If we want to access the `CUSTOM_SETTINGS_ENABLED` value we need to do it like this:

.. code-block:: python

	from sapyautomation.core import LazySettings
	
	LazySettings().CUSTOM_SETTINGS_ENABLED

File examples
^^^^^^^^^^^^^
.. list-table::
	:widths: 50 50
	:header-rows: 0
	
	* - .. code-block:: ini
			:caption: Default settings
			:name: default-settings
		
			[ENV]
			DEBUG = false
			CUSTOM_SETTINGS_ENABLED = false
			LOG_FILES_PATH = outputs/logs
			LOG_MAX_DAYS_KEEP = 100
			REPORT_FILES_PATH = outputs/reports
	  -	.. code-block:: ini
			:caption: Minimal settings
			:name: minimal-settings
			
			[ENV]
			CUSTOM_SETTINGS_ENABLED = False

		.. code-block:: ini
			:caption: Custom settings
			:name: custom-settings
		
			[ENV]
			CUSTOM_SETTINGS_ENABLED = True
		
			[CUSTOM]
			URL_FIORI = http://url

.. important:: To access custom settings inside your code you need to append 'CUSTOM' before the key, for example: ``LazySettings().CUSTOM_URL_FIORI``

Credentials
-----------
.. warning:: For security do not commit your **secrets.ini** to the git repository.

To simplify and secure the usage of credentials you can create a *secrets.ini*.

.. code-block:: ini
	:caption: Secrets example
	:name: secret-example

	[SAP]
	CLIENT=240
	USER=user
	PASSWORD=password
	LANGUAGE=EN
 
and access them using 'LazySettings':
 
.. code-block:: python
 
	credentials = LazySettings().CREDENTIALS('SAP')
	print(credentials['CLIENT'])

Basic Test Case Layout
----------------------
.. code-block:: python
	:caption: test case layout
	:name: case-example

	from sapyautomation.vendors.sap.test_enviroment import SapTestSuite
	
	
	class TestExample(SapTestSuite):
	
	    def setUp(self):
	        ...
	
	    def test_example(self):
	        self.step_login()
	        self.step_search()
	
	    def step_login(self):
	        ...
	        
	    def step_search(self):
	        ...
	    
	    def tearDown(self):
	        ...

Logger & Evidences
------------------

Inside your test case you have some utilities to enhance the reports.

Use ``self.log('message')`` inside you *steps* to add custom messages to the logger.

Use ``self.get_evidence()`` inside you *steps* to make an screenshot and add it to the report.


Test Data
----------

To avoid 'hard-coding' data to the test cases we can use ``TestData`` object like this: 

.. code-block:: python
	:caption: test data example
	:name: test-data-example
	
	from sapyautomation.core.test_cases import TestData

	book = TestData(self.data_file)
	sheet_data = book.data['FirstSheet']

	print(sheet_data['color'])
	
3rd Party Applications
----------------------

To add data on a 3rd party applicaton we can do it as it follows:

.. code-block:: python
	:caption: 3pa data example
	:name: 3pa-data-example
	
	self.add_3pa_data('test_id', 'test_name', 'system', 'description', 'category', 'process_team')
