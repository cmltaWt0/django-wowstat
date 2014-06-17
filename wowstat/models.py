from django.db import models
from datetime import datetime

class WowzaConnections(models.Model):
    """
    WowzaConnections(query_time=datetime.now, conn_counts)

    Model include creating time and connections count.
    Default value of query_time is datetime.now
    """
    query_time = models.DateTimeField(default=datetime.now)
    conn_counts = models.IntegerField()
