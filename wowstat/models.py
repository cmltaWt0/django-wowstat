from django.db import models
from datetime import datetime

class WowzaConnections(models.Model):
    query_time = models.DateTimeField(default=datetime.now)
    conn_counts = models.IntegerField()
