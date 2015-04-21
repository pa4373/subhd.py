Subhd.py: subhd.com Subtitle Downloader
=======================================

The tool downloads subtitles from subhd.com automatically, and in addition it performs:

  - decompress the archieve and guess the most possible one.
  - convert encoding to UTF-8 without BOM.
  - Unix line endings conversion.
  - convert to Traditional / Simplified Chinese (optional)

Python 3 support and Windows Testing is on schedule.

Installation
------------

Simply using pip:

:code:`$ pip install subhd.py`


or manual installation:

:code:`$ python setup.py install`

to decompress rar file, `unrar` is required.

Usage
-----

.. code-block:: shell

    $ subhd.py -h
    usage: subhd.py [-h] [-r] [-a] [-t TYPE] [-o OUTPUT] keyword [keyword ...]

    Download subtitle from subhd.com, with support for Traditional Chinese /
     Simplified Chinese, encoding conversion

    positional arguments:
      keyword               Specify source filename or keyword string

    optional arguments:
      -h, --help            show this help message and exit
      -r, --raw             Treat keyword as raw string instead of filename
      -a, --auto            Download subtitle without prompting (best guess)
      -t TYPE, --type TYPE  Type of operation, either 'zhs' or 'zht'
      -o OUTPUT, --output OUTPUT  Specify destination filename, default's prefix
                            is the same as filename

    Copyright (C) 2015 Wei-Shao Tang (Frank Tang)

    Web: https://github.com/pa4373/subhd.py

    This is free software; see the source for copying conditions.
    There is no warranty, not even for merchantability or fitness
    for a particular purpose.

For example, you can search a subtitle using filename:

.. code-block:: shell

   $ subhd.py Blade.Runner.1982.The.Final.Cut.BluRay.720p.DTS.2Audio.x264-CHD.mkv
   1) Blade Runner (final Cut)(1982) | 銀翼殺手 (None)
   2) Blade.Runner.1982.Final.Cut.BDRip.X264.iNT-TLF | 银翼杀手 导演最终剪辑版 (None)
   3) Blade Runner | 银翼杀手 | 公元2020/叛狱追杀令 (None)
   4) Blade Runner | 銀翼殺手 | 2020 (None)
   5) Blade Runner | 银翼杀手 | （好沉闷，看不懂！） (None)
   6) Dangerous Days: Making Blade Runner | 危险的日子：制作《银翼杀手》 (None)
   7) Blade Runner | 銀翼殺手 | 2020 (None)
   8) Blade Runner | 2020 | 银翼杀手 (None)
   9) Blade Runner | 银翼杀手 (None)
   10) Blade Runner | 银翼杀手 (None)
   11) Blade Runner | 银翼杀手 (None)
   12) Blade Runner | 银翼杀手 (None)
   13) Blade Runner | 银翼杀手 (None)
   14) Blade Runner | 銀翼殺手(國際院線版) (None)
   15) 银翼杀手 | Blade Runner | 导演剪辑版 修复版 | 銀翼殺手 (None)
   16) 银翼杀手 | Blade Runner (None)
   17) 银翼杀手 | Blade Runner (None)
   18) Blade.Runner | Blade.Runner.1982.Final.Cut.DVDRip.XviD-EPiC | 银翼杀手 (None)
   19) [银翼杀手].Blade.Runner.1982.HD-DVDRip.x264.a720.AC3-C@SiLU | Blade Runner | 银翼杀手 (None)
   20) 银翼杀手 | Blade Runner (None)
   Select one subtitle to download: 2

Then your subtitle is utf-8 encoded, translate to Tradtional Chinese and with proper srt index order.

To let the program automatically select subtitle for you, passing `-a` flags:

.. code-block:: shell

   $ subhd.py -a Blade.Runner.1982.The.Final.Cut.BluRay.720p.DTS.2Audio.x264-CHD.mkv

translateing to Simplified Chinese is possible, too:

.. code-block:: shell

   $ subhd.py -t zhs Blade.Runner.1982.The.Final.Cut.BluRay.720p.DTS.2Audio.x264-CHD.mkv

query as raw string instead of filename:

.. code-block:: shell

   $ subhd.py -r Blade\ Runner

Contributing
============
1. Fork it
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin my-new-feature)
5. Create new Pull Request

License
=======
The program is licensed under GNU GPL v3. You can obtain a online copy: https://www.gnu.org/licenses/gpl.txt
