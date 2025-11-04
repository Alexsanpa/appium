Run Test
========

For every test should exists at least one data-set file(xls, xlsx).

.. note:: Data set files should be named like this: <test_module_name>.xls or <uid>_<test_module_name>.xls 

To run specific tests this command should be used like this:

.. code-block:: bash

	python -m sapyautomation run_test <test.py> <parameters>

To discover tests this command should be used like this:

.. code-block:: bash

	python -m sapyautomation run_test discover <parameters>

Parameters
----------

--html-report
	Flag to generate html report

--xml-report
	Flag to generate xml report

--no-dataset
	Flag for test cases without dataset

-extra-resources=<path>
	This parameter adds one extra path to the search index in :meth:`sapyautomation.core.utils.general.get_resource`

-email-report name@server.com name@server.com ...
	This parameter specifies reciepts to send a email report of the execution

-m=<path>, --module-directory=<path>
	This parameter only works along ``discover`` and specifies the module to look for tests.
	
-d=<path>, --data-directory=<path>
	This parameter specifies the path to look for data set files.
	If this parameter isn't defined the default value will be: "resources/test_data/"
