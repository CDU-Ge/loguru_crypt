# -*- coding: utf-8 -*-
# Copyright (c) CDU

"""Model Docstrings

"""

from __future__ import absolute_import
from __future__ import annotations
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import pathlib

from loguru_crypt.rsa import RSA
from loguru_crypt.utils import exists_exit


def generate(password: str = None, directory: str = None):
    if password:
        password = password.encode("utf-8")
    if directory is not None:
        directory = pathlib.Path(directory)
        exists_exit(directory)
    RSA().generate(password)


def main():
    parser = argparse.ArgumentParser(description="Generate RSA keys with optional password and directory.")

    parser.add_argument("--password",
                        help="Password for RSA key (optional)", default=None)
    parser.add_argument("--directory",
                        type=pathlib.Path,
                        help="Directory to save RSA key (optional)", default=None)

    args = parser.parse_args()
    generate(args.password, args.directory)


if __name__ == '__main__':
    main()
