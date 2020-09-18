from cryptography.fernet import Fernet
import argon2
import base64
from utils.config import get_system_config

class EncryptUtils:
    salt = get_system_config()['salt_data']

    @staticmethod
    def encrypt_data(data_bytes, password):
        encoded_hash = EncryptUtils.encoded_hash(password)
        encrypt = Fernet(encoded_hash)
        return encrypt.encrypt(data_bytes)

    @staticmethod
    def decrypt_data(cipher_bytes, password):
        encoded_hash = EncryptUtils.encoded_hash(password)
        decrypt = Fernet(encoded_hash)
        return decrypt.decrypt(cipher_bytes)

    @classmethod
    def encoded_hash(cls, password):
        password_hash = argon2.argon2_hash(password=password, salt=cls.salt)
        return base64.urlsafe_b64encode(password_hash[:32])