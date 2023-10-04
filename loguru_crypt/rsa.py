# -*- coding: utf-8 -*-
# Copyright (c) CDU

"""Model Docstrings

"""

from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import base64
import os
import pathlib
from typing import *

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa

from loguru_crypt.utils import exists_exit

ORIGIN_MESSAGE = Union[bytes]
ENCRYPTED_MESSAGE = bytes
ORIGIN_BINARY = bytes
BASE64_STRING = str


class RSA:
    _public_exponent: Final = 65537
    _key_size: Final = 4096
    _chunk_size: Final = 128

    _OAEP = padding.OAEP(padding.MGF1(algorithm=hashes.SHA256()), hashes.SHA256(), None)  # noqa

    def __init__(self):
        self._private_key = None
        self._public_key = None

    def generate(self, password: bytes = None, directory: pathlib.Path = None):
        private_key = rsa.generate_private_key(public_exponent=self._public_exponent, key_size=self._key_size)

        if password is None:
            encryption_algorithm = serialization.NoEncryption()
        else:
            encryption_algorithm = serialization.BestAvailableEncryption(password)

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=encryption_algorithm  # noqa
        )

        public_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        if directory is None:
            private_key_path = os.path.join(os.getcwd(), "private_key.pem")
            public_key_path = os.path.join(os.getcwd(), "public_key.pem")
            exists_exit(private_key_path)
            exists_exit(public_key_path)

            with open(private_key_path, 'wb') as f:
                f.write(private_pem)

            with open(public_key_path, 'wb') as f:
                f.write(public_pem)

    def load_pem(self, t: Literal['raw', 'Path'], data: Union[bytes, str], private=True, passwd: bytes = None):
        if t == 'raw':
            if private:
                self._private_key = serialization.load_pem_private_key(data, passwd)
            else:
                self._public_key = serialization.load_pem_public_key(data)
        elif t == 'Path':
            if private:
                with open(data, 'rb') as f:
                    self._private_key = serialization.load_pem_private_key(f.read(), passwd)
            else:
                with open(data, 'rb') as f:
                    self._public_key = serialization.load_pem_public_key(f.read())

    @staticmethod
    def b64encode(data: ORIGIN_BINARY) -> BASE64_STRING:
        return base64.b64encode(data).decode('utf-8')

    @staticmethod
    def b64decode(data: BASE64_STRING) -> ORIGIN_BINARY:
        return base64.b64decode(data)

    def encrypt(self, message: ORIGIN_MESSAGE) -> ENCRYPTED_MESSAGE:
        if self._public_key is None:
            raise RuntimeError("The public key is missing")
        encrypted_message = self._public_key.encrypt(message, self._OAEP)
        return encrypted_message

    def decrypt(self, message: ENCRYPTED_MESSAGE) -> ORIGIN_MESSAGE:
        if self._private_key is None:
            raise RuntimeError("The private key is missing")
        decrypted_message = self._private_key.decrypt(message, self._OAEP)
        return decrypted_message

    def encrypt_message(self, message: str) -> str:
        message = f"{message}\n"
        message = message.encode(encoding='utf-8')
        if len(message) > self._chunk_size:
            message = "\n".join(map(self.b64encode, map(self.encrypt, [
                message[i:i + self._chunk_size] for i in range(0, len(message), self._chunk_size)
            ])))
        else:
            message = self.encrypt(message)
            message = self.b64encode(message)
        return message

    def decrypt_message(self, message: str) -> str:
        message = self.b64decode(message)
        message = self.decrypt(message)
        message = message.decode(encoding='utf-8')
        return message
