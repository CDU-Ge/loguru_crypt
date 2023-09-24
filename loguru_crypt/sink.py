# -*- coding: utf-8 -*-
# Copyright (c) CDU

"""Model Docstrings

"""

from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import pathlib
import sys
from typing import Callable
from typing import Optional
from typing import TYPE_CHECKING
from typing import TextIO
from typing import Union

if TYPE_CHECKING:
    from loguru import Message


class SimpleEncryptSink:
    def __init__(self, logfile: Union[str, pathlib.Path, TextIO], encrypt: Callable):
        self.logstream = None
        self.logfile = None
        self.logfile_stream: Optional[TextIO] = None
        if isinstance(logfile, TextIO):
            self.logstream = logfile
        elif logfile in [sys.stdout, sys.stderr]:
            self.logstream = logfile
        else:
            self.logfile = str(os.path.abspath(logfile))
        self.encrypt = encrypt

    def __enter__(self):
        self.logfile_stream = open(self.logfile, "a", encoding='utf-8')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.logfile_stream:
            self.logstream.close()
            self.logstream = None

    def write(self, message: Union['Message', str]):
        try:
            message = self.encrypt(message)
        except Exception as e:
            raise e
        message = f"{message}\n"
        if self.logstream and not self.logstream.closed:
            self.logstream.write(message)
        if self.logfile_stream:
            if not self.logfile_stream.closed:
                self.logfile_stream.write(message)
        else:
            if self.logfile:
                with open(self.logfile, "a", encoding="utf-8") as logfile:
                    logfile.write(message)
