from cryptography.fernet import Fernet
import argon2
import base64


class EncryptUtils:

    @staticmethod
    def encrypt_with_hash(data, hash):
        encrypt = Fernet(hash)
        return encrypt.encrypt(data.encode()).decode()

    @staticmethod
    def decrypt_with_hash(cipher, hash):
        decrypt = Fernet(hash)
        return decrypt.decrypt(cipher.encode()).decode()

    @staticmethod
    def encrypt_data(data, password, salt):
        if len(data) == 0:
            return ''
        encoded_hash = EncryptUtils.encoded_hash(password, salt)
        return EncryptUtils.encrypt_with_hash(data, encoded_hash)

    @staticmethod
    def decrypt_data(cipher, password, salt):
        if len(cipher) == 0:
            return ''
        encoded_hash = EncryptUtils.encoded_hash(password, salt)
        return EncryptUtils.decrypt_with_hash(cipher, encoded_hash)

    @classmethod
    def encoded_hash(cls, password, salt):
        password_hash = argon2.argon2_hash(password=password, salt=salt)
        return base64.urlsafe_b64encode(password_hash[:32])
