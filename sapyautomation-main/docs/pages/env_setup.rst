Environment Setup
=================

Creating a virtualenv
---------------------

It's highly recommended to create a virtualenv to work on.

We need to install *pipenv* to manage virtualenvs:

.. code:: bash

	pip install pipenv;

To enter a virtualenv we need to navigate to our project root path in a console and run:

.. note:: if is the first time you run pipenv in the current directory a new virtualenv will be created automagically.

.. code:: bash

	pipenv shell;

To exit the virtualenv you only need to use ``exit``.

.. note:: To add the virtualenv to your IDE you can find the virtualenv in ``C:\Users\<USER>\.virtualenvs\``

Installing sapyautomation
-------------------------

To install the framework we need to add our repository to the pip configuration, for that we are going to use a devpi util command wich we need to install first:

.. code:: bash

	pip install devpi-client;

Now we add the repository as it follows:

.. code:: bash

	devpi use http://sapy-automation.com:8081;
	devpi use --set-cfg sapy/staging;
	devpi use --always-set-cfg=yes;

.. note:: You can also use the **sapy/stable** or **sapy/dev** repository.

and then install the package normally:

.. code:: bash

	pip install sapyautomation;
