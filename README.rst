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

