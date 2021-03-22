from cryptography.fernet import Fernet
from jwt import encode, decode


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)


def jwt_encode(uuid, code):
    encoded_jwt = encode({"uuid": uuid, "code": code}, 'vmember', algorithm='HS256')

    return encoded_jwt


def jwt_decode(token):
    decoded_jwt = decode(token, 'vmember', algorithms=['HS256'])

    return decoded_jwt