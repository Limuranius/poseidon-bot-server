from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Логин от сайта ДВФУ
    FEFU_username = models.CharField(max_length=100)

    # Пароль от сайта ДВФУ
    FEFU_password = models.CharField(max_length=100)

    # Пароль от сайта ДВФУ. Хранится в зашифрованном виде, поэтому BinaryField
    # FEFU_password = models.BinaryField()

    # Соль, используемая вместе с мастер-паролем(паролем у CustomUser) для получения шифровального ключа
    # FEFU_password_salt = models.BinaryField()
    #
    # def get_decrypted_FEFU_password(self) -> str:
    #     crypter = PasswordEncrypter(
    #         self.FEFU_username,
    #         self.FEFU_password_salt
    #     )