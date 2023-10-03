# -*- coding: utf-8 -*-
# Copyright (c) CDU

"""Model Docstrings

"""

from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import pathlib
from logging import getLogger
from typing import Callable
from typing import TYPE_CHECKING
from typing import Union

if TYPE_CHECKING:
    from loguru import Message


class SimpleEncryptSink:
    def __init__(self, logfile: Union[str, pathlib.Path], encrypt: Callable):
        self.logger = getLogger('loguru_crypt')
        self.logger.propagate = False
        self.logger.setLevel(logging.ERROR)
        self.logger_file = logging.FileHandler(logfile, encoding='utf-8')
        self.logger_file.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(self.logger_file)
        self.encrypt = encrypt

    def write(self, message: Union['Message', str]):
        try:
            message = self.encrypt(message)
        except Exception as e:
            raise e
        message = f"{message}"
        self.logger.error(message)
