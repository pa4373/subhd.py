#!/usr/bin/env python
import core
import argparse
import re
from guessit import guess_video_info
from core import SubHDDownloader
from compressor import ZIPFileHandler, RARFileHandler
from sanitizer import to_unicode, to_chs, to_cht, reset_index, set_utf8_without_bom

EPILOG = '''
Copyright (C) 2015 Wei-Shao Tang (Frank Tang)

Web: https://github.com/pa4373/subhd.py

This is free software; see the source for copying conditions.
There is no warranty, not even for merchantability or fitness
for a particular purpose.
'''

'''
python 3 support 
windows support
'''

compressor_handler = {
    'rar': RARFileHandler,
    'zip': ZIPFileHandler
}

def get_subtitle(keyword, is_filename=True, auto_download=False, chiconv_type='zht', out_file=None):
    downloader = SubHDDownloader()
    if is_filename:
        filename = keyword
        video_info = guess_video_info(keyword)
        keyword = video_info.get('title') or video_info.get('series') # using type might be better
    results = downloader.search(keyword)
    if not results:
        print "No subtitle for %s" % keyword
        return

    # Choose subtitle (if not auto download)
    choice = None
    if not auto_download:
        indexes = range(len(results))
        for i in indexes:
            item = results[i]
            print '%s) %s (%s)' % (i+1, item.get('title'), item.get('org'))
        while not choice:
            try:
                choice = int(raw_input("Select one subtitle to download: "), 10)
            except ValueError:
                print 'Error: only numbers accepted'
                continue
            if not (choice - 1) in indexes:
                print 'Error: numbers not within the range'
                choice = None
        choice = results[choice - 1]
    else:
        choice = results[0]

    # Download sub here.
    datatype, sub_data = downloader.download(choice.get('id'))
    file_handler = compressor_handler.get(datatype)
    if file_handler:
        compressor = file_handler(sub_data)
        subtitle_name, subtitle_body = compressor.extract_bestguess()
        subtitle_name = './' + subtitle_name
        subtitle_extension = subtitle_name.split('.')[-1]

    # Chinese conversion
    subtitle_body = to_unicode(subtitle_body) # Unicode object
    if chiconv_type == 'zht':
        subtitle_body = to_cht(subtitle_body)
    elif chiconv_type == 'zhs':
        subtitle_body = to_chs(subtitle_body)

    if subtitle_extension == 'srt':
        subtitle_body = reset_index(subtitle_body)

    subtitle_body = set_utf8_without_bom(subtitle_body) # Plain string
    subtitle_body = subtitle_body.replace('\r\n', '\n') # Unix line endings
    
    if is_filename:
        extension = filename.split('.')[-1]
        subtitle_name = filename.replace(extension, 'zh.%s' % subtitle_extension)
    if out_file:
        subtitle_name = out_file

    f = open(subtitle_name, 'w')
    f.write(subtitle_body)
    f.close()
        
def tongwen_check(v):
    if not v in ('zht', 'zhs'):
        raise argparse.ArgumentError('Type of operation, either \'zhs\' or \'zht\'')
    return v

if __name__ == '__main__':
    usage_help = 'Download subtitle from subhd.com, with support for ' \
                 'Traditional Chinese / \n Simplified Chinese, encoding conversion'
    arg_parser = argparse.ArgumentParser(description=usage_help, epilog=EPILOG,
                                         formatter_class=argparse.RawTextHelpFormatter)
    arg_parser.add_argument('-r', '--raw', action='store_true',
                            help='Treat keyword as raw string instead of filename')
    arg_parser.add_argument('-a', '--auto', action='store_true',
                            help='Download subtitle without prompting (best guess)')
    arg_parser.add_argument('-t', '--type', type=tongwen_check, default='zht',
                            help='Type of operation, either \'zhs\' or \'zht\'')
    arg_parser.add_argument('-o', '--output',
                            help='Specify destination filename, default\'s prefix\n is the same as filename')
    arg_parser.add_argument('keyword', nargs='+',
                            help='Specify source filename or keyword string')
    
    args = arg_parser.parse_args()
    try:
        if args.raw:
            keywords = [' '.join(args.keyword)]
        else:
            keywords = args.keyword
            
        for keyword in  keywords:
            get_subtitle(keyword, is_filename=(not args.raw),
                         auto_download=args.auto,
                         chiconv_type=args.type, out_file=args.output)
    except KeyboardInterrupt:
        exit()
