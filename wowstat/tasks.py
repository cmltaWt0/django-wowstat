from __future__ import absolute_import

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from httplib2 import Http
import ConfigParser
import xml.etree.ElementTree as etree

from .models import WowzaConnections
from datetime import datetime

from django.conf import settings
PATH = settings.PROJECT_PATH

config = ConfigParser.RawConfigParser()
config.read(PATH + '/../conf.ini')
server_ip = config.get('wowza', 'server_ip')
server_port = config.get('wowza', 'server_port')
login = config.get('wowza', 'login')
password = config.get('wowza', 'password')

from webssc import celery_app

@celery_app.task(expires=60)
def wowlog():
    """Query user connections info from Wowza streaming server and save to DB.
    """

    h = Http()
    h.add_credentials(login, password)

    root = etree.fromstring(h.request('http://' + server_ip + ':' + server_port +
                            '/connectioncounts/')[1])

    value = int(root[0].text)
    WowzaConnections.objects.create(query_time=datetime.now(), conn_counts=value)

    return str(value)


@celery_app.task
def logging(*args, **kwargs):
    with open('log_file', 'a') as l:
        l.write(args[0]+'\n')


