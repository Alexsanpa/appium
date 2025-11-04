Init Test
=========

This command generates a python class skeeleton for tests cases from a collection file(xls, xlsx).

.. note:: Data set files should be named like this: collection_<collection_name>.xls

To run specific tests this command should be used like this:

To generate a test skeeleton run the follow command.
 
.. code-block:: bash

	python -m sapyautomation init_test <tests_id> -c <collection_name> -m <module>

You can add multiple <test_id> to mass generation.

Parameters
----------

--collection
	Collection file name

-t=<path>, --target-environment=<path>
	This parameter adds one extra path to the search index in :meth:`sapyautomation.core.utils.general.get_resource`

-m=<path>, --module-directory=<path>
	Specifies in which module the skeeleton will be save to.

-d=<path>, --data-directory=<path>
	This parameter specifies the path to look for collection files.