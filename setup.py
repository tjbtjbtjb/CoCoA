# -*- coding: utf-8 -*-

""" 
Project : CoCoA
Date :    april/may 2020
Authors : Olivier Dadoun, Julien Browaeys, Tristan Beau
Copyright © CoCoa-team-17
License: See joint LICENSE file

About : mandatory setup file
"""

from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='CoCoA',
    url='https://github.com/tjbtjbtjb/CoCoA',
    author='Olivier Dadoun, Julien Browaeys, Tristan Beau',
    author_email='odadoun@gmail.com,browaeys@gmail.com,tristan.beau@gmail.com',
    # Needed to actually package something
    packages=['cocoa','cocoaplot'],
    # Needed for dependencies
    install_requires=['numpy','requests','pandas','matplotlib','bokeh','plotly','branca','folium','geopy','altair','lxml'],
    # *strongly* suggested for sharing
    version='0.2',
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. See
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=3.5, <4',
    # The license can be anything you like
    license='MIT',
    description='CoCoA stands for COvid COlab Analysis project, which is an open source project initially designed to run in the Google colab environment.',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)
