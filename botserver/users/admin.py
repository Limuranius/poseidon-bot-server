from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Register your models here.

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser

    list_display = ("username", "FEFU_username", "FEFU_password")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("FEFU credentials", {"fields": ("FEFU_username", "FEFU_password")})
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "FEFU_username", "FEFU_password")
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
