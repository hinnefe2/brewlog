"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

setup(
    name='brewlog',  # Required

    version='1.0.0',  # Required

    description='Webapp for logging Aeropress brews',  # Required

    url='https://aerobrewlog.herokuapp.com/',  # Optional

    author='Henry Hinnefeld',  # Optional

    author_email='henry.hinnefeld@gmail.com',  # Optional

    packages=find_packages(),  # Required

    project_urls={  # Optional
        'Webapp': 'https://aerobrewlog.herokuapp.com/',
        'Source': 'https://github.com/hinnefe2/brewlog',
    },
)
