#!/usr/bin/bash

#service nginx start
service mysql start
#service php7.4-fpm start

python3 site/server.py
