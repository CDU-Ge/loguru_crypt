import pathlib
import unittest

from loguru import logger

from loguru_crypt.rsa import RSA
from loguru_crypt.sink import SimpleEncryptSink

logger.remove()
rsa = RSA()
rsa.load_pem('Path', '../public_key.pem', False)
logger.add(SimpleEncryptSink("test.log", rsa.encrypt_message), level='DEBUG')


class MyTestCase(unittest.TestCase):
    def test_base(self):
        logger.error('test!')
        self.assertEqual(True,
                         pathlib.Path('test.log').read_bytes() != b"")

    def test_read(self):
        rsa.load_pem('Path', '../private_key.pem', True, b'1234')
        list(map(print, map(rsa.decrypt_message,
                            filter(None, pathlib.Path('test.log').read_text().splitlines())
                            )))


if __name__ == '__main__':
    unittest.main()
