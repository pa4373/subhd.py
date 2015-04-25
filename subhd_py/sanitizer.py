'''Few sanitizer functions to process subtitle text.
'''
import chardet
from pyTongwen.conv import TongWenConv
import StringIO
import pysrt

__TONGWEN = TongWenConv()

def to_unicode(sub_str):
    '''Convert plain string to unicode object.

    Auto encoding converison occurs if the plain string isn't encoded
    in UTF-8.

    Args:
        sub_str: The plain string intended to be converted to unicode
                 object
    Returns:
        sub_unicode: The converted unicode object

    '''
    encoding = chardet.detect(sub_str).get('encoding')
    if encoding:
        sub_unicode = unicode(sub_str, encoding, 'ignore')
    return sub_unicode

def to_cht(sub_unicode):
    '''Convert any Chinese unicode strings to Tradtional Chinese

    Args:
        sub_unicode: any Chinese unicode object
    Returns:
        sub_unicode: unicode object converted to Tradtional Chinese

    '''
    return __TONGWEN.conv_zh(sub_unicode, 'zht')

def to_chs(sub_unicode):
    '''Convert any Chinese unicode strings to Simplified Chinese

    Args:
        sub_unicode: any Chinese unicode object
    Returns:
        sub_unicode: unicode object converted to Simplified Chinese

    '''
    return __TONGWEN.conv_zh(sub_unicode, 'zhs')

def set_utf8_without_bom(sub_unicode):
    '''Convert a unicode object to plain string.

    Remove BOM header if exists

    Args:
        sub_unicode: any unicode object intended to be converted
                     to string
    Returns:
        sub_str: Plain string encoded in UTF-8 without BOM
    '''
    if sub_unicode.startswith(u'\ufeff'):
        sub_unicode = sub_unicode[3:]
    sub_str = sub_unicode.encode('utf-8')
    return sub_str

def reset_index(sub_unicode):
    '''Reset SRT subtitles index.

    The subtitle index increases incrementally from 1.

    Args:
        sub_unicode: unicode object containing SRT subtitles
    Returns:
        new_sub_unicode: Reordered unicode SRT object.

    '''
    subs = pysrt.from_string(sub_unicode)
    for i in range(1, len(subs) + 1):
        subs[i - 1].index = i

    new_sub = StringIO.StringIO()
    subs.write_into(new_sub)
    new_sub_unicode = new_sub.getvalue()
    new_sub.close()
    return new_sub_unicode
'''Few sanitizer functions to process subtitle text.
'''
import chardet
import codecs
from pyTongwen.conv import TongWenConv
import StringIO
import pysrt

__TONGWEN = TongWenConv()

def to_unicode(sub_str):
    '''Convert plain string to unicode object.

    Auto encoding converison occurs if the plain string isn't encoded
    in UTF-8.

    Args:
        sub_str: The plain string intended to be converted to unicode
                 object
    Returns:
        sub_unicode: The converted unicode object

    '''
    encoding = chardet.detect(sub_str).get('encoding')
    if encoding:
        sub_unicode = unicode(sub_str, encoding, 'ignore')
    return sub_unicode

def to_cht(sub_unicode):
    '''Convert any Chinese unicode strings to Tradtional Chinese

    Args:
        sub_unicode: any Chinese unicode object
    Returns:
        sub_unicode: unicode object converted to Tradtional Chinese

    '''
    return __TONGWEN.conv_zh(sub_unicode, 'zht')

def to_chs(sub_unicode):
    '''Convert any Chinese unicode strings to Simplified Chinese

    Args:
        sub_unicode: any Chinese unicode object
    Returns:
        sub_unicode: unicode object converted to Simplified Chinese

    '''
    return __TONGWEN.conv_zh(sub_unicode, 'zhs')

def set_utf8_without_bom(sub_unicode):
    '''Convert a unicode object to plain string.

    Remove BOM header if exists

    Args:
        sub_unicode: any unicode object intended to be converted
                     to string
    Returns:
        sub_str: Plain string encoded in UTF-8 without BOM
    '''
    sub_str = sub_unicode.encode('utf-8')
    if sub_str[:3] == codecs.BOM_UTF8:
        sub_str = sub_str[3:]
    return sub_str

def reset_index(sub_unicode):
    '''Reset SRT subtitles index.

    The subtitle index increases incrementally from 1.

    Args:
        sub_unicode: unicode object containing SRT subtitles
    Returns:
        new_sub_unicode: Reordered unicode SRT object.

    '''
    subs = pysrt.from_string(sub_unicode)
    for i in range(1, len(subs) + 1):
        subs[i - 1].index = i

    new_sub = StringIO.StringIO()
    subs.write_into(new_sub)
    new_sub_unicode = new_sub.getvalue()
    new_sub.close()
    return new_sub_unicode
