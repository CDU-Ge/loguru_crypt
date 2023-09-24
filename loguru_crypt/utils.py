# -*- coding: utf-8 -*-
# Copyright (c) CDU

"""Model Docstrings

"""

from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pathlib
import sys
from typing import Union


def exists_exit(filepath: Union[str, pathlib.Path]):
    if isinstance(filepath, str):
        filepath = pathlib.Path(filepath)
    if filepath.exists():
        print(f"{filepath.name} exists !", file=sys.stderr)
        sys.exit(-1)
