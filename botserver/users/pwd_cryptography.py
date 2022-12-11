from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os


"""
Пароль от ДВФУ шифруется:
    - При регистрации пользователя (UserCreationsForm)
    - При изменении пользователем своего пароля (UserChangeForm) (изменяет либо мастер-пароль, либо ДВФУ пароль, либо оба)

Пароль от ДВФУ расшифруется:
    - При отправлении ботом запроса на сайт ДВФУ
        До этого бот создаётся и ему передаётся дешифратор с мастер-паролем
        Но при запуске сервера все существующие боты должны как-то запускаться без мастер-пароля
"""


# Сколько итераций хеширования нужно произвести над паролем, чтобы затем полученный хеш перевести в ключ
ITERATIONS_FOR_KEY = 100000  # НЕ ИЗМЕНЯТЬ БЕЗ РЕЗКОЙ НЕОБХОДИМОСТИ. ПОЛЕТИТ ВСЁ ШИФРОВАНИЕ ДЛЯ СОЗДАННЫХ РАННЕЕ ПАРОЛЕЙ


def _hash_password(password: str, salt: bytes, iterations: int) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode())


def _password_to_key(password: str, salt: bytes) -> bytes:
    """Преобразует мастер пароль + соль в шифровальный ключ, используемый для шифровки / расшифровки паролей"""
    hashed_pwd = _hash_password(password, salt, ITERATIONS_FOR_KEY)
    key = base64.urlsafe_b64encode(hashed_pwd)
    return key


def _generate_salt() -> bytes:
    """Генерирует соль(набор случайных байтов), используемую при хешировании паролей"""
    return os.urandom(16)


class PasswordEncrypter:
    """
    Используется для шифровки / расшифровки паролей с помощью мастер-пароля и его соли
    """
    __crypter: Fernet

    def __init__(self, master_password: str, salt: bytes):
        self.__crypter = Fernet(_password_to_key(master_password, salt))

    def encrypt_password(self, password: str) -> bytes:
        """Зашифровывает пароль password в набор байтов"""
        return self.__crypter.encrypt(password.encode())

    def decrypt_password(self, encrypted_password: bytes) -> str:
        """Расшифровывает пароль password в изначальную строку"""
        return self.__crypter.decrypt(encrypted_password).decode()
