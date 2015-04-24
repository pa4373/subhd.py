#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'subhd.py',
    version = '0.1.2',
    description = 'subhd.com subtitle downloader',
    author = 'Wei-Shao Tang (Frank Tang)',
    author_email = 'pa4373@gmail.com',
    url = 'https://github.com/pa4373/subhd.py',
    download_url = 'https://github.com/pa4373/subhd.py/tarball/0.1.2',
    license = 'GPLv3',
    scripts = ['bin/subhd.py'],
    packages = ['subhd_py'],
    keywords='subtitle subtitles video movie episode tv show',
    install_requires = [
        'beautifulsoup4==4.3.2',
        'chardet==2.3.0',
        'guessit==0.9.4',
        'pysrt==1.0.1',
        'rarfile==2.7',
        'requests==2.6.0',
        'six==1.9.0',
        'tongwen-python==1.0.0'
    ],
    dependency_links = [
        'https://codeload.github.com/pa4373/tongwen-python/zip/master#egg=tongwen-python-1.0.0'
    ]
)
