#!/usr/bin/env python3

from setuptools import setup, find_packages
from os import path

SCRIPTDIR = path.abspath(path.dirname(__file__))

with open(path.join(SCRIPTDIR, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
                             name = "csvmagic",
                      description = "CSV Utilities",
                          version = "1.0.1",
                          license = "Apache 2.0",
                           author = "Mark Kim",
                     author_email = "markuskimius+py@gmail.com",
                              url = "https://github.com/markuskimius/csvmagic",
                         keywords = [ "csv", "text" ],
                 long_description = long_description,
    long_description_content_type = "text/markdown",
                          scripts = [
                                        "bin/csvalign",
                                        "bin/csvcsv",
                                        "bin/csvcut",
                                        "bin/csvgrep",
                                        "bin/csvread",
                                        "bin/csvsql",
                                    ],
                       data_files = [
                                        ("man/man1", [
                                            "man/man1/csvalign.1",
                                            "man/man1/csvcsv.1",
                                            "man/man1/csvcut.1",
                                            "man/man1/csvgrep.1",
                                            "man/man1/csvread.1",
                                            "man/man1/csvsql.1",
                                        ])
                                    ],
                         packages = find_packages("lib"),
                      package_dir = { "": "lib" },
                 install_requires = [ "getopts" ],
)
