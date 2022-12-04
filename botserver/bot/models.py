from django.db import models


class RecordModel(models.Model):
    open_time = models.TimeField()
    date = models.DateField()
    min_duration = models.TimeField()
    max_duration = models.TimeField()
    machine_number = models.IntegerField()
    time_from = models.TimeField()
    time_before = models.TimeField()
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)
