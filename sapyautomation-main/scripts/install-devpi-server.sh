#!/bin/bash
echo -e "\e[96m
##########################
# devpi install          #
# ---------------------- #
# execute as root (sudo) #
##########################
\e[39m"

echo -e "\e[95m[system]\e[39m running initial cleanup..."
service devpi stop
userdel devpi
groupdel devpi
rm -f /etc/systemd/system/devpi.service /etc/nginx/nginx.conf
rm -rf /opt/devpi /root/.devpi
yum remove nginx -y -q
yum autoremove -y -q
set -e # exit on error, print executed commands
DEVPI_VENV=/opt/devpi
DEVPI_USER=devpi
args=(
	--system
	--shell $(which nologin)
	--home ${DEVPI_VENV}
	--no-create-home
	--user-group
	--comment "DevPI server"
	)
	
echo -e "\e[95m[system]\e[39m creating devpi user..."
useradd ${DEVPI_USER} "${args[@]}"
passwd --lock ${DEVPI_USER}

echo -e "\e[95m[system]\e[39m creating devpi environment..."
mkdir ${DEVPI_VENV}
chown ${DEVPI_USER}:${DEVPI_USER} ${DEVPI_VENV}
yum install -y -q python3-pip python3-devel


echo -e "\e[93mdevpi installation\e[39m"
read -p '(control-c to abort, enter to continue)' continue
cat > ${DEVPI_VENV}/devpi.yaml <<-EOF
devpi-server:
  serverdir: ${DEVPI_VENV}/data
  host: localhost
  port: 4040
EOF

echo -e "\e[95m[devpi]\e[39m initial setup..."
sudo -u ${DEVPI_USER} bash -ec "
	cd ${DEVPI_VENV}
	python3 -m venv  ${DEVPI_VENV}
	source ${DEVPI_VENV}/bin/activate
	pip install -U devpi-server --no-cache-dir --quiet
	pip install -q -U devpi-web --no-cache-dir --quiet
	pip install -U --pre -q devpi-client --no-cache-dir  --quiet
	
	devpi-init -c ${DEVPI_VENV}/devpi.yaml
	devpi-gen-config -c ${DEVPI_VENV}/devpi.yaml
"
echo -e "\e[95m[devpi]\e[39m creating service..."
cp ${DEVPI_VENV}/gen-config/devpi.service /etc/systemd/system/
systemctl daemon-reload
service devpi start
yum remove -y -q python3-devel
yum autoremove -y -q


echo -e "\e[93mnginx installation\e[39m"
read -p '(control-c to abort, enter to continue)' continue
amazon-linux-extras install nginx1
sudo chkconfig nginx on

echo -e "\e[95m[nginx]\e[39m cleanup..."
service nginx stop
rm -f /etc/nginx/nginx.conf

echo -e "[nginx] adding devpi conf..."
cp ${DEVPI_VENV}/gen-config/nginx-devpi.conf /etc/nginx/nginx.conf
nano /etc/nginx/nginx.conf

echo -e "\e[95m[nginx]\e[39m launching service..."
service nginx start

echo -e "\e[93mfirst run\e[39m"
read -p '(control-c to abort, enter to continue)' continue
${DEVPI_VENV}/bin/devpi use http://localhost:8081
${DEVPI_VENV}/bin/devpi use -l


echo -e "\e[93mpassword for devpi-user\e[39m"
read -sp '[root]:' rootpass
${DEVPI_VENV}/bin/devpi login root --password ''
${DEVPI_VENV}/bin/devpi user -m root password=$rootpass


echo -e "\e[93mpassword for devpi-user\e[39m"
read -sp '[sapy]:' sapypass
${DEVPI_VENV}/bin/devpi user -c sapy password=$sapypass
${DEVPI_VENV}/bin/devpi index -c sapy/stable bases=root/pypi volatile=False
${DEVPI_VENV}/bin/devpi index -c sapy/staging bases=sapy/stable volatile=True
${DEVPI_VENV}/bin/devpi index -c sapy/dev bases=sapy/staging volatile=True

echo -e "\e[96m
#########################
# Installation finished #
#########################
\e[39m"