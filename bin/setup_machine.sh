#!/usr/bin/env bash

read -n 1 -s -r -p "Press any key to start the configuration."

# Pull File Upload Server
echo "Finding FileUploadServer folder..."

localFolder="/home/ubuntu/FileUploadServer"

if [ ! -d $localFolder ]; then

    echo "Couldn't find folder FileUploadServer. Cloning..."

    fileUploadRepo="https://github.com/ArpanSriv/FileUploadServer.git"

    hash git 2>/dev/null || { echo >&2 "I require git but it's not installed.  Aborting."; exit 1; }

    git config --global user.email "arpansri98@gmail.com"
    git config --global user.name "Arpan Srivastava"

    git clone $fileUploadRepo $localFolder

fi

# Setup Main Django Server
# Setup venv
(
    cd /home/ubuntu/hackathon-website

    apt-get install python3-pip virtualenv

    sudo -u ubuntu virtualenv --python=python3 venv

    source venv/bin/activate

    sudo -u ubuntu venv/bin/pip install -r requirements.txt

)

echo "[STATUS]: Setup of venv complete.."

cp /home/ubuntu/hackathon-website/bin/services/gunicorn_django.service /etc/systemd/system/

systemctl enable gunicorn_django.service
systemctl start gunicorn_django.service
systemctl status gunicorn_django.service

# install nginx
apt-get install nginx

ip=$(dig TXT +short o-o.myaddr.l.google.com @ns1.google.com | awk -F'"' '{ print $2}')

sed -e "s;%IP_ADDR%;$ip;g" nginx/hackathon-nginx-template > nginx/hackathon.vhost

cp nginx/hackathon.vhost /etc/nginx/sites-available/hackathon.vhost
ln -s /etc/nginx/sites-available/hackathon.vhost /etc/nginx/sites-enabled/hackathon.vhost

service nginx restart

echo "IP is ${ip}"

if [ $HENV eq 'prod' ]; then
    echo "Running prod only config.."
    
    read -n 1 -s -r -p "Press any key to continue"

    apt-get update
    apt-get install software-properties-common
    add-apt-repository universe
    add-apt-repository ppa:certbot/certbot
    apt-get update

    apt-get install certbot python-certbot-nginx 

    certbot --nginx
fi