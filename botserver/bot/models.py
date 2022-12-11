from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class RecordModel(models.Model):
    open_datetime = models.DateTimeField()
    date = models.DateField()
    min_duration = models.TimeField()
    max_duration = models.TimeField()
    machine_number = models.IntegerField()
    time_from = models.TimeField()
    time_before = models.TimeField()
    user_name = models.CharField(max_length=50)
    log = models.TextField(blank=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse("record_url", kwargs={"record_id": self.pk})
