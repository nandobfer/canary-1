#!/usr/bin/bash

#service nginx start
service mysql start
#service php7.4-fpm start
cd site
python3 -c 'import server; server.run()'
