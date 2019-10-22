# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'bet_parser',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = bet_parser.settings']},
)
