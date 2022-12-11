from django import forms
from .models import RecordModel


class RecordForm(forms.ModelForm):
    class Meta:
        model = RecordModel
        fields = ["open_datetime", "date", "min_duration",
                  "max_duration", "machine_number", "time_from",
                  "time_before", "user_name"]

        widgets = {
            "open_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "date": forms.DateInput(attrs={"type": "date"}),
            "min_duration": forms.DateInput(attrs={"type": "time", "step": 900}),
            "max_duration": forms.DateInput(attrs={"type": "time", "step": 900}),
            "time_from": forms.DateInput(attrs={"type": "time", "step": 900}),
            "time_before": forms.DateInput(attrs={"type": "time", "step": 900}),
        }

        labels = {
            "open_datetime": "Запись открывается в",
            "date": "Дата",
            "min_duration": "Минимальная длительность",
            "max_duration": "Максимальная длительность",
            "machine_number": "Номер машинки",
            "time_from": "Искать от",
            "time_before": "Искать до",
            "user_name": "Имя",
        }