Automated activities
====================

There are some activities that are automated with tox.

Static Analysis
---------------

To make static analysis you can use:

``tox -e analysis``

or run manually:

.. code:: bash

    flake8;
    pylint sapyautomation --extension-pkg-whitelist=cv2;

Unitary Tests
-------------

To make unitary tests you can use:

``tox -e tests``

or run manually:

.. code:: bash

    coverage run -m unittest;
    coverage report;

Documentation Generation
------------------------

To generate this documentation you can use:

``tox -e docs`` or ``tox -e docs37``

or run manually:

.. code:: bash

	sphinx-apidoc -fTe -d 0 -o docs/apidoc sapyautomation;
	sphinx-build -b html docs docs/build;

Unestable Package Building
--------------------------

To build and upload the unestable version:

``tox -e builddev``

or run manually:

.. code:: bash

	devpi use http://ec2-3-130-29-109.us-east-2.compute.amazonaws.com:8081;
	devpi login sapy --password=<password>;
	devpi use -l;
	devpi use sapy/dev;
	devpi upload --formats sdist,sdist.zip,bdist_wheel;

Stage Package Building
----------------------

To build and upload the stage version:

``tox -e buildstage``

or run manually:

.. code:: bash

	devpi use http://ec2-3-130-29-109.us-east-2.compute.amazonaws.com:8081;
	devpi login sapy --password=<password>;
	devpi use -l;
	devpi use sapy/staging;
	devpi upload --formats sdist,sdist.zip,bdist_wheel;

Stable Package Building
-----------------------

To build and upload the stable version:

``tox -e buildstable``

or run manually:

.. code:: bash

	devpi use http://ec2-3-130-29-109.us-east-2.compute.amazonaws.com:8081;
	devpi login sapy --password=<password>;
	devpi use -l;
	devpi use sapy/stable;
	devpi upload --formats sdist,sdist.zip,bdist_wheel;
