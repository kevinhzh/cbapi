# -*- encoding: utf-8 -*-
"""
@File    :   setup.py
@Time    :   2020/08/24
@Author  :   Kevin Huang
@Version :   1.0
"""

from setuptools import setup
from os import path
import io

here = path.abspath(path.dirname(__file__))

with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with io.open(path.join(here, "requirements.txt"), encoding='utf-8') as f:
    requires = f.read().split()

setup(
    name="cbapi",
    version="0.1.0",
    description="An API to get organization and people data from Crunchbase.",
    long_description=long_description,
    url="https://github.com/kevinhzh/cbapi",
    author="Kevin Huang",
    author_email="kevinhzh97@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    platforms=["any"],
    keywords="cbapi, Crunchbase, RapidAPI",
    packages=["cbapi"],
    install_requires=requires,
)