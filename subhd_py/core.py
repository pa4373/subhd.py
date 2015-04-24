# -*- coding: utf-8 -*-
'''This module defines SubHDDownloader class, the core communication
 part with subhd.com.
'''
import re
import requests
from StringIO import StringIO
from urllib import quote
from bs4 import BeautifulSoup

class SubHDDownloader(object):
    '''The class seeks and downloads subtitles from subhd.com
    '''
    def __init__(self):
        self.dl_lookup_url = 'http://subhd.com/ajax/down_ajax'
        self.search_url = 'http://subhd.com/search/'
        self.subid_re = re.compile(r'^/a/(\d+)$')
        self.org_re = re.compile(r'^/zu/(\d+)$')
        self.info_re = re.compile(ur'\u683c\u5f0f\uff1a(\S+)\s' +
                                  ur'\u7248\u672c\uff1a(\S+)',
                                  re.UNICODE)

    def search(self, keyword):
        '''Search subtitles candidates.

        Args:
            keyword: the keyword to search, can be given as the filename
        Returns:
            items: a list of dictionaries containing: subtitle id, title,
                   subtitle format and corrsponding video version.

        '''
        escaped_keyword = quote(keyword)
        page = requests.get(self.search_url + escaped_keyword)
        soup = BeautifulSoup(page.content)

        page_list = soup.find(class_='col-md-9').childGenerator()
        items = []
        for i in page_list:
            try:
                item = {}
                hrefs = i.find_all('a')
                for j in hrefs:
                    match = self.subid_re.match(j.get('href'))
                    if match and j.get('target'):
                        item['id'] = match.group(1)
                        item['title'] = j.getText()
                    match = self.org_re.match(j.get('href'))
                    if match:
                        item['org'] = j.getText()

                item_text = i.getText()
                match = self.info_re.search(item_text)
                if match:
                    item['format'], item['version'] = match.groups()

                if item != {}:
                    items.append(item)
            except AttributeError: # The field might be '\n', ' ' or whatever
                pass
        return items

    def download(self, subtitle_id):
        '''Downlaod the subtitle archive with archive type.

        Args:
            subtitle_id: the id of the subtitle.
        Returns:
            datatype: file format of the archive. (rar, zip, srt)
            sub_data: binary data of the archive.

        '''
        payload = {
            'sub_id': int(subtitle_id)
        }
        res_with_real_addr = requests.post(self.dl_lookup_url, data=payload)
        try:
            res_with_real_addr = res_with_real_addr.json()
            real_addr = res_with_real_addr.get('url')
            if not real_addr:
                print 'No url.'
        except ValueError:
            print 'No subtitle download'

        sub_datastring = requests.get(real_addr).content
        if len(sub_datastring) < 1024:
            datatype = None
        if sub_datastring[:4] == 'Rar!':
            datatype = 'rar'
        elif sub_datastring[:2] == 'PK':
            datatype = 'zip'
        else:
            datatype = 'srt'

        sub_buff = StringIO()
        sub_buff.write(sub_datastring)
        return (datatype, sub_buff)
