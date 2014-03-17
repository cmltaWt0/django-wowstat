#TODO Move all this logic to Celery or somenthing else in DJANGO
# Import settings is not working without django ENV.


#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Wowlog make a connection to wowza server
   and get an appropriate url to retrive connections
   information.
   Then insert this info into database.
"""

import os
#import time
#import sqlite3
import psycopg2
import httplib2
import ConfigParser
import xml.etree.ElementTree as etree

######################################################################
# For sqlite3
# sqlite3 wowstat.db
# CREATE TABLE summary (id INTEGER, time, counts, PRIMARY KEY(id ASC));
#######################################################################
# For postrgesql
# createdb test_wowstat
# psql test_wowstat
# CREATE TABLE summary (id BIGSERIAL PRIMARY KEY, query_time timestamp, conn_counts integer);
#######################################################################

#hour = str(time.localtime().tm_hour)
#minuts = str(time.localtime().tm_min)

from django.conf import settings
PATH = settings.PROJECT_PATH

config = ConfigParser.RawConfigParser()
config.read(PATH + '/../conf.ini')
server_ip = config.get('wowza', 'server_ip')
server_port = config.get('wowza', 'server_port')
login = config.get('wowza', 'login')
password = config.get('wowza', 'password')
postgres_ip = config.get('postgresql', 'ip')
postgres_user = config.get('postgresql', 'user')
postgres_pass = config.get('postgresql', 'pass')

h = httplib2.Http()
h.add_credentials(login, password)

root = etree.fromstring(h.request('http://' + server_ip + ':' + server_port +
    	                '/connectioncounts/')[1])

######################################################
# For sqlite
#conn = sqlite3.connect(PATH + '/wowstat.db')
#######################################################
# For postresql
conn = psycopg2.connect("dbname='wowstat' user={0} password={1} host={2}"
                        .format(postgres_user, postgres_pass, postgres_ip))
######################################################
# Common
cur = conn.cursor()
######################################################
# Postgres
cur.execute("INSERT INTO summary (query_time, conn_counts) VALUES ('now', %s)",
	        (int(root[0].text),))
######################################################
# Sqlite3
#cur.execute("INSERT INTO summary VALUES (null, ?, ?)",
#	        (hour+':'+minuts, root[0].text))
######################################################
# Common
conn.commit()
cur.close()
conn.close()

# chmod +x path_to_project/ssc/webssc/wowstat/wowlog.py
# */10 *  * * *   user  path_to_project/ssc/webssc/wowstat/wowlog.py

