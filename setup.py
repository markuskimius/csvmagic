#!/usr/bin/env python3

from setuptools import setup, find_packages
from os import path

SCRIPTDIR = path.abspath(path.dirname(__file__))

with open(path.join(SCRIPTDIR, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
                             name = "csvutils",
                      description = "CSV Utilities",
                          version = "1.0.0",
                          license = "Apache 2.0",
                           author = "Mark Kim",
                     author_email = "markuskimius+py@gmail.com",
                              url = "https://github.com/markuskimius/csvutils",
                         keywords = [ "csv", "text" ],
                 long_description = long_description,
    long_description_content_type = "text/markdown",
                          scripts = [
                                        "bin/csvsql",
                                        "bin/csvcsv",
                                        "bin/csvcut",
                                        "bin/csvalign",
                                        "bin/csvgrep",
                                        "bin/csvread",
                                    ],
                         packages = find_packages("lib"),
                      package_dir = { "": "lib" },
                         requires = [ "getopts" ],
)
