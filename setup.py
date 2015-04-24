#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'subhd.py',
    version = '0.1',
    description = 'subhd.com subtitle downloader',
    author = 'Wei-Shao Tang (Frank Tang)',
    author_email = 'pa4373@gmail.com',
    url = 'https://github.com/pa4373/subhd.py',
    download_url = 'https://github.com/pa4373/subhd.py/tarball/0.1',
    license = 'GPLv3',
    scripts = ['bin/subhd.py'],
    packages = ['subhd_py'],
    keywords='subtitle subtitles video movie episode tv show',
    install_requires= open('requirements.txt').readlines(),
    dependency_links = [
        'https://codeload.github.com/pa4373/tongwen-python/zip/master#egg=tongwen-python-1.0.0'
    ]
)
