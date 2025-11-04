#!/bin/bash
echo -e "\e[96m
##########################
# upgrade docs           #
# ---------------------- #
# execute as root (sudo) #
##########################
\e[39m"
set -e # exit on error, print executed commands

DEVPI_VENV=/opt/devpi
DEVPI_USER=devpi
BRANCH=${1:-develop}

yum install git
cd ${DEVPI_VENV}
git clone -b $BRANCH http://ec2-3-130-29-109.us-east-2.compute.amazonaws.com/Knuth/sapyautomation.git
cd sapyautomation

source ${DEVPI_VENV}/bin/activate
pip install Sphinx sphinx-theme autodoc

sphinx-apidoc -fTe -d 0 -o docs/apidoc sapyautomation
sphinx-build -b html docs docs/build

rm -Rf ${DEVPI_VENV}/data/documentation/*
mv ${DEVPI_VENV}/sapyautomation/docs/build/* ${DEVPI_VENV}/data/documentation/

rm -Rf ${DEVPI_VENV}/sapyautomation
echo "add location '/documentation/' like this:
    location /documentation/ {
        root /opt/devpi/data/documentation/;
        index.html
    }
"
read -p '(control-c to abort, enter to continue)' continue
nano /etc/nginx/nginx.conf
service nginx restart
echo -e "\e[96m
#########################
# upgrade finished      #
#########################
\e[39m"