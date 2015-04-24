#!/usr/bin/env python
'''Main program for subhd.py
'''
import argparse
from guessit import guess_video_info
from subhd_py.core import SubHDDownloader
from subhd_py.compressor import ZIPFileHandler, RARFileHandler
from subhd_py.sanitizer import to_unicode, to_chs, to_cht, reset_index, set_utf8_without_bom

EPILOG = '''
Copyright (C) 2015 Wei-Shao Tang (Frank Tang)

Web: https://github.com/pa4373/subhd.py

This is free software; see the source for copying conditions.
There is no warranty, not even for merchantability or fitness
for a particular purpose.
'''

COMPRESSPR_HANDLER = {
    'rar': RARFileHandler,
    'zip': ZIPFileHandler
}

CHICONV = {
    'zhs': to_chs,
    'zht': to_cht
}

DOWNLOADER = SubHDDownloader()

def choose_subtitle(candidates):
    '''Console output for choosing subtitle.

    Args:
        candidates: A list of dictionaries of subtitles.
    Returns:
        candidate: One dictionary within the list.

    '''
    indexes = range(len(candidates))
    for i in indexes:
        item = candidates[i]
        print '%s) %s (%s)' % (i+1, item.get('title'), item.get('org'))
    choice = None
    while not choice:
        try:
            choice = int(raw_input("Select one subtitle to download: "), 10)
        except ValueError:
            print 'Error: only numbers accepted'
            continue
        if not choice - 1 in indexes:
            print 'Error: numbers not within the range'
            choice = None
    candidate = candidates[choice - 1]
    return candidate

def get_guessed_video_name(video_name):
    '''Parse the video info from the filename

    Args:
        video_name: the filename of the video
    Returns:
        keyword: return video title, usually as movie name,
                 otherwise the series title, usually as drama name.

    '''
    video_info = guess_video_info(video_name)
    return video_info.get('title') or video_info.get('series')

def get_subtitle(keyword, is_filename=True, auto_download=False,
                 chiconv_type='zht', out_file=None):
    '''The main function of the program.

    Args:
        keyword: the keyword to query, either as filename or raw string.
        is_filename: boolean value indicates the keyword is filename or not.
        auto_download: skip all interactive query if it's turn on
        chiconv_type: either 'zhs' or 'zht'
        out_file: optional, the destination path of subtitle.

    Returns:
    '''
    if is_filename:
        filename = keyword
        keyword = get_guessed_video_name(filename)

    results = DOWNLOADER.search(keyword)
    if not results:
        print "No subtitle for %s" % keyword
        return

    if not auto_download:
        target = choose_subtitle(results)
    else:
        target = results[0]

    # Download sub here.
    datatype, sub_data = DOWNLOADER.download(target.get('id'))
    file_handler = COMPRESSPR_HANDLER.get(datatype)
    compressor = file_handler(sub_data)

    subtitle = {} # record for subtitle
    subtitle['name'], subtitle['body'] = compressor.extract_bestguess()
    subtitle['name'] = './' + subtitle['name'].split('/')[-1]
    subtitle['extension'] = subtitle['name'].split('.')[-1]

    # Chinese conversion
    subtitle['body'] = to_unicode(subtitle['body']) # Unicode object
    conv_func = CHICONV.get(chiconv_type)
    subtitle['body'] = conv_func(subtitle['body'])

    if subtitle['extension'] == 'srt':
        subtitle['body'] = reset_index(subtitle['body'])

    subtitle['body'] = set_utf8_without_bom(subtitle['body']) # Plain string
    subtitle['body'] = subtitle['body'].replace('\r\n', '\n') # Unix-style line endings

    if not out_file:
        if not is_filename:
            filename = subtitle['name']
        out_file = filename.replace(filename.split('.')[-1],
                                    'zh.%s' % subtitle['extension'])

    with open(out_file, 'w') as subfile:
        subfile.write(subtitle['body'])
    return

def tongwen_check(value):
    '''TongWen conversion type check.

    Args:
        value: the value to be checked. Raise an exception if test fails.
    Returns:
        value: the value either 'zht' or 'zhs'

    '''
    if not value in ('zht', 'zhs'):
        raise argparse.ArgumentError('Type of operation, either \'zhs\' or \'zht\'')
    return value

def main():
    '''Main entry point of the program.

    Primarily for argument parsing. No arguments and return values.

    '''
    usage = 'Download subtitle from subhd.com, with support for ' \
            'Traditional Chinese / \n Simplified Chinese, encoding conversion'
    arg_parser = argparse.ArgumentParser(description=usage, epilog=EPILOG,
                                         formatter_class=argparse.RawTextHelpFormatter)
    arg_parser.add_argument('-r', '--raw', action='store_true',
                            help='Treat keyword as raw string instead of filename')
    arg_parser.add_argument('-a', '--auto', action='store_true',
                            help='Download subtitle without prompting (best guess)')
    arg_parser.add_argument('-t', '--type', type=tongwen_check, default='zht',
                            help='Type of operation, either \'zhs\' or \'zht\'')
    arg_parser.add_argument('-o', '--output',
                            help='Specify destination filename, default\'s prefix\n' \
                            ' is the same as filename')
    arg_parser.add_argument('keyword', nargs='+',
                            help='Specify source filename or keyword string')

    args = arg_parser.parse_args()
    try:
        if args.raw:
            keywords = [' '.join(args.keyword)]
        else:
            keywords = args.keyword

        for keyword in keywords:
            get_subtitle(keyword, is_filename=(not args.raw),
                         auto_download=args.auto,
                         chiconv_type=args.type, out_file=args.output)
    except KeyboardInterrupt:
        exit()

if __name__ == '__main__':
    main()
