#!/bin/bash
echo -e "\e[96m
##########################
# install python 38      #
# ---------------------- #
# execute as root (sudo) #
##########################
\e[39m"
yum install gcc openssl-devel bzip2-devel libffi-devel;
cd /opt;
wget https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tgz;
tar xzf Python-3.8.2.tgz;
cd Python-3.8.2;
./configure --enable-optimizations;
make altinstall;
cd ..;
rm -f /opt/Python-3.8.2.tgz;
sudo rm -R /opt/Python-3.8.2;
echo -e "\e[96m
#########################
# installation finished #
#########################
\e[39m"
