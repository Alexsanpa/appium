Resume Test
===========

To resume specific tests this command should be used like this:

.. code-block:: bash

	python -m sapyautomation resume_test <test.py> <parameters>

To discover paused tests this command should be used like this:

.. code-block:: bash

	python -m sapyautomation resume_test discover <parameters>

Parameters
----------

--html-report
	Flag to generate html report

--xml-report
	Flag to generate xml report

-extra-resources=<path>
	This parameter adds one extra path to the search index in :meth:`sapyautomation.core.utils.general.get_resource`

-email-report name@server.com name@server.com ...
	This parameter specifies reciepts to send a email report of the execution