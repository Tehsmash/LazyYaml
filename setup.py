#!/usr/bin/env python

from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


def requirements():
    with open('requirements.txt') as rf:
        return rf.readlines()


setup(name='lazyyaml',
      author='Sam Betts',
      author_email='sam@code-smash.net',
      summary='A lazy yaml processor which allows for Jinja2 templated items',
      description=readme(),
      install_requires=requirements(),
      url='https://github.com/Tehsmash/LazyYaml',
      packages=find_packages(),
      entry_points={'console_scripts': 'lazyyaml=lazyyaml.cli:main'},
      version='0.0.1-dev')
