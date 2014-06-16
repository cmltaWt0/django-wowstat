=======
Wowstat
=======

Wowsat is a simple Django app to conduct Web-based Wowza server statistic.

Quick start
-----------

1. Add "wowstat" to your INSTALLED_APPS setting like this::

       INSTALLED_APPS = (
          ...
          'wowstat',
       )

2. Include the polls URLconf in your project urls.py like this::

    url(r'^wowstat/', include('wowstat.urls')),

    BROKER_URL = 'redis://localhost'
    CELERY_RESULT_BACKEND = 'redis://localhost'

    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT=['json']
    CELERY_TIMEZONE = 'Europe/Kiev'
    CELERY_ENABLE_UTC = True


    from datetime import timedelta

    CELERYBEAT_SCHEDULE = {
        'add-every-300-seconds': {
            'task': 'wowstat.tasks.wowlog',
            'schedule': timedelta(seconds=300)
        },
    }

3. Create or change conf.ini file in root of your django project to add next::

    [wowza]
    server_ip = 
    server_port = 
    login = 
    password =

    [postgresql]
    ip = 
    user = 
    pass = 


4. Install redis::

    pip install redis

5. Install and run Celery::

    pip install celery
    celery -A webssc worker -B

