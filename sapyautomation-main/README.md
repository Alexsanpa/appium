[![pipeline status](https://www.sapy-automation.com/Knuth/sapyautomation/badges/develop/pipeline.svg)](https://www.sapy-automation.com/Knuth/sapyautomation/-/commits/develop) Sapy Automation
==============

Python library to automate the Microsoft Windows GUI, SAP flows and browser.


[[_TOC_]]

Project Links
-------------

* [Documentation](http://sapy-automation.com:8081/documentation/)
* [Devpi Repository](http://sapy-automation.com:8081/)

Run tests
---------

In order to do unitary tests run the follow:

	`tox -e tests`

or manually:

```
pip install -r requirements.txt;

coverage run -m unittest discover;

coverage report;
```

Static code analysis
--------------------

In order to do static analysis run the follow:

	`tox -e analysis`

or manually:

```
pip install -r tests-requirements.txt;

flake8;

pylint sapyautomation --extension-pkg-whitelist=cv2;
```

Documentation generation
------------------------

In order to generate documentation run the follow:

	`tox -e docs`

or manually:

```
pip install -r test-requirements.txt;

sphinx-apidoc -fTe -d 0 -o docs/apidoc sapyautomation;

sphinx-build -b html docs docs/build;
```

Package building & upload
-------------------------

In order to upload the package run the follow:

	`tox -e buildstage`

or manually:

```
pip install devpi-client;

devpi use <server_url>;

devpi login sapy --password <password>;

devpi use sapy/staging;

devpi upload;
```

The package would be builded when `devpi upload` is called.

Installing package
------------------

If you want to install sapyautomation with `pip` you need to add the repository first:

```
devpi use http://ec2-3-130-29-109.us-east-2.compute.amazonaws.com:8081;

devpi use --set-cfg sapy/staging;

devpi use --always-set-cfg=yes;
```

and then install the package:

```
pip uninstall sapyautomation;

pip install sapyautomation --no-cache-dir;
```
