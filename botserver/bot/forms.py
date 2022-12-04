from django import forms
from .models import RecordModel


class RecordForm(forms.ModelForm):
    class Meta:
        model = RecordModel
        fields = ["open_time", "date", "min_duration",
                  "max_duration", "machine_number", "time_from",
                  "time_before", "login", "password", "user_name"]

        widgets = {
            "open_time": forms.TimeInput(attrs={"type": "time"}),
            "date": forms.DateInput(attrs={"type": "date"}),
            "min_duration": forms.DateInput(attrs={"type": "time", "step": 900}),
            "max_duration": forms.DateInput(attrs={"type": "time", "step": 900}),
            "time_from": forms.DateInput(attrs={"type": "time", "step": 900}),
            "time_before": forms.DateInput(attrs={"type": "time", "step": 900}),
            "password": forms.DateInput(attrs={"type": "password"}),
        }

        labels = {
            "open_time": "Запись открывается в",
            "date": "Дата",
            "min_duration": "Минимальная длительность",
            "max_duration": "Максимальная длительность",
            "machine_number": "Номер машинки",
            "time_from": "Искать от",
            "time_before": "Искать до",
            "login": "Логин от ДВФУ",
            "password": "Пароль от ДВФУ",
            "user_name": "Имя",
        }
