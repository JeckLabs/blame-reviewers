# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="blame-reviewers",
    version="0.1.1",
    description="CLI tool for searching code reviewers from git blame.",
    license="MIT",
    author="Evgeniy Baranov",
    packages=find_packages(),
    install_requires=[
        'sh>=1.12.13,<2'
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        'console_scripts': [
            'blame-reviewers = reviewers.__main__:main'
        ]
    },
)
