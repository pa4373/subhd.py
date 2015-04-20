import chardet
from pyTongwen.conv import TongWenConv
import StringIO
import pysrt

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
    if sub_str.startswith(u'\ufeff'):
        sub_str = sub_str[3:]
    sub_str = sub_str.encode('utf-8')
    return sub_str
    
def reset_index(sub_str):
    subs = pysrt.from_string(sub_str)
    for i in range(1, len(subs) + 1):
        subs[i - 1].index = i
    new_sub = StringIO.StringIO()
    subs.write_into(new_sub)
    new_substring = new_sub.getvalue()
    new_sub.close()
    return new_substring
