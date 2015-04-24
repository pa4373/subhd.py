# -*- encoding:utf-8 -*-


# conv.py
#
# Copyright 2010 swatch
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#



import word
import phrase
import codecs
import os.path
import re


class TongWenConv:
    def __init__(self, path=None):
        self.utable_path = path #path of user phrase file
        self.ps2t = {}
        self.pt2s = {}
        self.ps2t_precount = {}
        self.pt2s_precount = {}
        self.ups2t = {} 
        self.upt2s = {}

    def init_precount(self,zhtab):
        p = {}
        for k in zhtab:
            p[k[0:2]] = 2
        for k in zhtab:
            if len(k) > p[k[0:2]]:
                p[k[0:2]] = len(k)
        return p

    def init_user_phrase(self,path):
        if os.path.exists(path) == False:
            return None, None
        f = codecs.open(path,encoding='utf-8')
        s_flg = 0
        u_s2t = {}
        u_t2s = {}
        for line in f:
            if line.startswith('<traditional>'):
                s_flg = 0
            elif line.startswith('<simplified>'):
                s_flg = 1
            elif line.startswith('<phrase>'):
                p = re.sub(r'<phrase><s>(.*)</s><r>(.*)</r></phrase>\s+', r'\1</s><r>\2', line)
                l = p.split('</s><r>')
                if s_flg == 0:
                    u_s2t[l[0]] = l[1]
                else:
                    u_t2s[l[0]] = l[1]
        f.close()
        return u_s2t, u_t2s

    def init_tongwen_table(self, u_flg):
        self.ps2t = {}
        self.pt2s = {}
        for key in phrase.s2t.keys():
            self.ps2t[key] = phrase.s2t[key]
        for key in phrase.t2s.keys():
            self.pt2s[key] = phrase.t2s[key]
        if u_flg == True:
            self.ups2t, self.upt2s = self.init_user_phrase(self.utable_path)
            if self.ups2t:
                for key in self.ups2t.keys():
                    if len(key) > 2 and key[0:2] not in self.ps2t.keys():
                        self.ps2t[key[0:2]] = key[0:2]
                    self.ps2t[key] = self.ups2t[key]
            if self.upt2s:
                for key in self.upt2s.keys():
                    if len(key) > 2 and key[0:2] not in self.pt2s.keys():
                        self.pt2s[key[0:2]] = key[0:2]
                    self.pt2s[key] = self.upt2s[key]
        self.ps2t_precount = self.init_precount(self.ps2t)
        self.pt2s_precount = self.init_precount(self.pt2s)        

    def get_user_table(self):
        return self.ups2t, self.upt2s
        
    def conv_zh(self,text,zhflg):
        if zhflg == 'zht':
            zhmap = word.s2t
            #zhtab = phrase.s2t
            zhtab = self.ps2t
            zhmax = self.ps2t_precount
        elif zhflg == 'zhs':
            zhmap = word.t2s
            #zhtab = phrase.t2s
            zhtab = self.pt2s
            zhmax = self.pt2s_precount

        text = list(text)
        for i in range(0,len(text)):
            if text[i] in zhmap:
                text[i] = zhmap[text[i]]

        i=0
        while i < len(text)-1:
            s = "".join(text[i:i+2])
            if s not in zhtab:
                i += 1
                continue
            m = zhmax[s]
            j = m
            while j >= 2:
                if "".join(text[i:i+j]) in zhtab:
                    text[i:i+j] = zhtab["".join(text[i:i+j])]
                    i += j
                    break
                j -= 1

        text = "".join(text)
        return text
