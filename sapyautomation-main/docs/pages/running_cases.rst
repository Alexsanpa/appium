Running Test Cases
==================

To run your cases you can use the framework's CLI utility.

If you want to run specific cases you can put all the files to run:

.. code-block:: python

	python -m sapyautomation run_test <case>.py <case2>.py <case3>.py

To run all the cases in the project you can use ``discover`` command:

.. code-block:: python

	python -m sapyautomation run_test discover

If you want to generate a report in html format you need to use ``--html-report`` flag:

.. code-block:: python

	python -m sapyautomation run_test <case>.py --html-report

Getting Data From Cases
-----------------------
When you run a case 'A' data can be added to the result so you can retrieve it from a case 'B'

To this feat to work properly in the case 'A' you need to add data to the result, first you need to save data to a class variable and then use the ``add_to_result`` method:

.. code-block:: python

	self.my_data = 'data'
	...
	self.add_to_result('my_data')

if the case 'A' execution ends in success then you can retrive in case 'B' the data added to the result like this:

.. code-block:: python

	a_data = self.get_case_data('TestCaseAClassName')
	a_data['my_data']

Pausing & Resuming Cases
------------------------

There are some cases that needs to be paused, for that we have decorator that helps to indicate conditional pauses.

When you run a case using the follow decorators it will stop a save a 'paused' status so you can resume then later.
To the decorators to work properly only will be used on *step* methods.

Time pause
^^^^^^^^^^
.. note:: The decorator ``pause_until`` allows as parameter *hours*, *days* and *minutes*.

When you want to pause the case for a specific amount of time you can do it as it follows:

.. code-block:: python
	:caption: time pause example
	:name: time-pause-example

	from sapyautomation.vendors.sap.test_enviroment import SapTestSuite
	from sapyautomation.core.test_cases.decorators import pause_until
	
	
	class TestExample(SapTestSuite):
	
	    def setUp(self):
	        ...
	
	    def test_example(self):
	        self.step_login()
	        self.step_search()
	
	    def step_login(self):
	        ...
	        
	    @pause_until(hours=1, reason='time')
	    def step_search(self):
	        ...
	    
	    def tearDown(self):
	        ...

Conditional pause
^^^^^^^^^^^^^^^^^

When you want to pause the case for a conditional motive you can create a method outside your case that returns a boolean value and use it like this:

.. code-block:: python
	:caption: conditional pause example
	:name: conditional-pause-example

	from sapyautomation.vendors.sap.test_enviroment import SapTestSuite
	from sapyautomation.core.test_cases.decorators import pause_if
	
	def x_file_dont_exists()
		...

	class TestExample(SapTestSuite):
	
	    def setUp(self):
	        ...
	
	    def test_example(self):
	        self.step_login()
	        self.step_search()
	
	    def step_login(self):
	        ...
	        
	    @pause_if(x_file_dont_exists(), reason='file')
	    def step_search(self):
	        ...
	    
	    def tearDown(self):
	        ...

Resume paused cases
^^^^^^^^^^^^^^^^^^^

To resume the paused cases you need to replace the ``run_test`` CLI command with ``resume_test``, the usage is exactly the same.
