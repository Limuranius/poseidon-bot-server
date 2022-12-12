from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "password1", "password2", "FEFU_username", "FEFU_password")
        widgets = {
            "FEFU_password": forms.PasswordInput()
        }

        labels = {
            "username": "Логин",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
            "FEFU_username": "Логин от сайта ДВФУ",
            "FEFU_password": "Пароль от сайта ДВФУ",
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ("username", "password", "FEFU_username", "FEFU_password")
