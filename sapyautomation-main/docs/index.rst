Welcome to Sapy's documentation!
================================

.. sidebar:: Project Links

	* `Documentation <http://sapy-automation.com:8081/documentation/>`_
	* `Devpi Repository <http://sapy-automation.com:8081/>`_
	* `Gitlab Repository <http://sapy-automation.com/>`_

Python library to automate the Microsoft Windows GUI, SAP flows and browser.

Indices and tables
^^^^^^^^^^^^^^^^^^

* :ref:`genindex`
* :ref:`modindex`

.. toctree::
	:hidden:
	:maxdepth: 2
	:caption: Guides:
	
	pages/first_steps
	pages/settings
	pages/framework_dev
	pages/cli_commands

.. toctree::
	:hidden:
	:maxdepth: 1
	:caption: Quick References:
	
	indexes/pom
	indexes/test_suite

.. toctree::
	:hidden:
	:maxdepth: 1
	:caption: Packages:

	apidoc/sapyautomation.core
	apidoc/sapyautomation.web
	apidoc/sapyautomation.desktop
	apidoc/sapyautomation.vendors

:doc:`changelog`
----------------
30/12/2020
	* added ``--no-dataset`` parameter to cli commands: :doc:`pages/run_test`
	* New Classes for API test cases in :meth:`sapyautomation.vendors.rest.test_enviroment.RestTestSuite` and :meth:`sapyautomation.vendors.rest.test_enviroment.RestBasePom`

13/05/2020
	* added ``await_before`` and ``await_after`` to :meth:`sapyautomation.core.test_cases.bases.BaseTestCases.get_evidence`
    * New cli commands: :meth:`sapyautomation.core.management.commands.init_test`

07/05/2020
	* added ``start_record`` and ``stop_record`` to :meth:`sapyautomation.core.test_cases.bases.BaseTestCases`
	* added :meth:`sapyautomation.desktop.screen.ScreenCapture` for better evidences.

04/05/2020
	* added element's management objects :meth:`sapyautomation.vendors.sap.actions.ElementById`, :meth:`sapyautomation.vendors.sap.actions.ElementByName`, :meth:`sapyautomation.vendors.sap.actions.ElementByLabel`
	* added ``wait_time`` parameter to :meth:`sapyautomation.core.test_cases.bases.BaseTestCases.get_evidence`
	* added ``-d <path>`` parameter for data set files discover
	* added grouped execution by data sets. 

30/04/2020
	* added evidences pdf report to when ``--html-report`` is used.
	* added ``-m <path>`` parameter to discover for module-specific tests discover
	* fixed discover parameter for :doc:`pages/run_test` and :doc:`pages/resume_test`
	* enabled optional combine reports with setting variable ``COMBINE_REPORTS``

22/04/2020
	* added :meth:`sapyautomation.vendors.sap.test_enviroment.SapTestSuite.change_login`
	* added :meth:`sapyautomation.vendors.sap.login.Login.logout`

21/04/2020
	* added '-email-report' parameter to cli commands: :doc:`pages/run_test`, :doc:`pages/resume_test`
	* added 3rd party applications registry to :meth:`sapyautomation.desktop.files.generate_unique_filename` and :meth: `sapyautomation.core.test_cases.base.BaseTestCases.add_3pa_data`
	* added general use methods :meth:`sapyautomation.desktop.files.generate_unique_filename` and :meth: `sapyautomation.desktop.files.generate_unique_dirname`

17/04/2020
	* added object: :meth:`sapyautomation.core.test_cases.models.TestData`
	* added '-extra-resources' parameter to cli commands: :doc:`pages/run_test`, :doc:`pages/resume_test`  

06/04/2020
	* New cli commands: :meth:`sapyautomation.core.management.commands.start_sap`, :meth:`sapyautomation.core.management.commands.stop_sap`.
	* Added default credentials load in :meth:`sapyautomation.vendors.sap.test_enviroment.SapTestSuite.login`
	* Added :meth:`sapyautomation.core.utils.connection.send_email`
