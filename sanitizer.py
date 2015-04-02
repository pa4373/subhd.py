import chardet
from pyTongwen.conv import TongWenConv

__tongwen = TongWenConv()

def to_unicode(sub_str):
    encoding = chardet.detect(sub_str).get('encoding')
    if encoding:
        sub_str = unicode(sub_str, encoding, 'ignore')
    return sub_str

def to_cht(sub_str):
    return __tongwen.conv_zh(sub_str, 'zht')

def to_chs(sub_str):
    return __tongwen.conv_zh(sub_str, 'zhs')

def set_utf8_without_bom(sub_str):
    pass

def set_unix_newline(sub_str):
    pass

def reset_index(sub_str):
    pass
