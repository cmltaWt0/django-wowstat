# -*- coding: utf-8 -*-

import httplib2
import ConfigParser
import xml.etree.ElementTree as etree
from django.template.response import TemplateResponse

from django.views.generic import View

from datetime import datetime, date, timedelta

from forms import DateChoices
from models import WowzaConnections


from django.conf import settings
PATH = settings.PROJECT_PATH

config = ConfigParser.RawConfigParser()
config.read(PATH + '/../conf.ini')
server_ip = config.get('wowza', 'server_ip')
server_port = config.get('wowza', 'server_port')
login = config.get('wowza', 'login')
password = config.get('wowza', 'password')

wowza_get_string = 'http://85.90.192.233:8001/cams/pathkey=cam'
velton_video_path = 'http://velton.ua/ru/'

translate = {
    'veltonMedium46.stream': ('Поле Металлист. Низкое качество',
        wowza_get_string + '1', velton_video_path + 'metallist/Wide1HQ.shtml'),
    'veltonQuality46.stream': ('Поле Металлист. Высокое качество',
        wowza_get_string + '1', velton_video_path + 'metallist/Wide1HQ.shtml'),
    'veltonMedium47.stream': ('Детская площадка. Низкое качество',
        wowza_get_string + '2', velton_video_path + 'metallist/Wide2HQ.shtml'),
    'veltonQuality47.stream': ('Детская площадка. Высокое качество',
        wowza_get_string + '2', velton_video_path + 'metallist/Wide2HQ.shtml'),
    'veltonMedium48.stream': ('Вид на Металлист. Низкое качество',
        wowza_get_string + '3', velton_video_path + 'metallist/Wide1HQ.shtml'),
    'veltonQuality48.stream': ('Вид на Металлист. Высокое качество',
        wowza_get_string + '3', velton_video_path + 'metallist/Wide1HQ.shtml'),
    'veltonMedium49.stream': ('Пл. свободы. Низкое качество',
        wowza_get_string + '4', velton_video_path + 'webcams/Wide1HQ.shtml'),
    'veltonQuality49.stream': ('Пл. свободы. Высокое качество',
        wowza_get_string + '4', velton_video_path + 'webcams/Wide1HQ.shtml'),
    'veltonMedium50.stream': ('Донецк. Низкое качество',
        wowza_get_string + '5', velton_video_path + 'webcams/Wide2HQ.shtml'),
    'veltonQuality50.stream': ('Донецк. Высокое качество',
        wowza_get_string + '5', velton_video_path + 'webcams/Wide2HQ.shtml'),
    'veltonMedium51.stream': ('Днепропетровск. Низкое качество',
        wowza_get_string + '1', velton_video_path + 'webcams/Wide1HQ.shtml'),
    'veltonQuality51.stream': ('Днепропетровск. Высокое качество',
        wowza_get_string + '1', velton_video_path + 'webcams/Wide1HQ.shtml'),
    'veltonMedium52.stream': ('Одесса. Низкое качество',
        wowza_get_string + '8', velton_video_path + 'webcams/Wide5HQ.shtml'),
    'veltonQuality52.stream': ('Одесса. Высокое качество',
        wowza_get_string + '8', velton_video_path + 'webcams/Wide5HQ.shtml'),
    'veltonMedium53.stream': ('Полтава. Низкое качество',
        wowza_get_string + '6', velton_video_path + 'webcams/Wide3HQ.shtml'),
    'veltonQuality53.stream': ('Полтава. Высокое качество',
        wowza_get_string + '6', velton_video_path + 'webcams/Wide3HQ.shtml'),
    'veltonMedium54.stream': ('Зеркальная струя. Низкое качество',
        wowza_get_string + '7', velton_video_path + 'webcams/Wide4HQ.shtml'),
    'veltonQuality54.stream': ('Зеркальная струя. Высокое качество',
        wowza_get_string + '7', velton_video_path + 'webcams/Wide4HQ.shtml'),
    'veltonMedium55.stream': ('Киев. Низкое качество',
        wowza_get_string + '1', velton_video_path + 'webcams/Wide1HQ.shtml'),
    'veltonQuality55.stream': ('Киев. Высокое качество',
        wowza_get_string + '1', velton_video_path + 'webcams/Wide1HQ.shtml')
}


def wowza(request, date_choice):
    """
    Make a connection to wowza server, retrieve
    /connectioncounts url and get detailed connections info.
    Then select summary info about last two days connection info.
    """
    h = httplib2.Http()
    h.add_credentials(login, password)
    try:
        root = etree.fromstring(h.request('http://' + server_ip + ':' +
                                server_port + '/connectioncounts/')[1])
    except Exception as e:
        return TemplateResponse(request, 'wowstat/error.html', {'err': str(e)})

    detail = []
    cams_dict = {}
    # Find streams info in returned xml.
    for child in (root.find('VHost').find('Application').
                  find('ApplicationInstance').findall('Stream')):
        # Save total session information
        detail.append([child.findall('Name')[0].text,
                       child.findall('SessionsTotal')[0].text])

    for i in detail:  # change stream name (name.stream) to human readable
        if i[0] in translate:
            cams_dict[translate[i[0]][1]] = translate[i[0]][2]
            i[0] = translate[i[0]][0]

    if date_choice == date.today():
        w = WowzaConnections.objects.filter(query_time__gt=datetime.now()-timedelta(days=1)).extra(order_by=['query_time'])
    else:
        w = WowzaConnections.objects.filter(query_time__day=date_choice.day,
                                            query_time__month=date_choice.month,
                                            query_time__year=date_choice.year).extra(order_by=['query_time'])

    summary = []
    for i in w:
        summary.append([i.query_time, i.conn_counts])

    return {'summary': summary, 'detail': detail, 'current': root[0].text,
            'cams_dict': cams_dict}


class Dispatcher(View):
    def get(self, request):
        form, date_choice = DateChoices(), date.today()
        return self.render(request, form, date_choice)

    def post(self, request):
        form = DateChoices(request.POST)
        if form.is_valid():
            date_choice = form.cleaned_data['date_choice']
        else:
            date_choice = date.today()
        return self.render(request, form, date_choice)

    @staticmethod
    def render(request, form, date_choice):
        response = wowza(request, date_choice)
        response['form'] = form
        response['date_choice'] = date_choice

        return TemplateResponse(request, 'wowstat/wowza.html', response)
