#/usr/bin/env python
import core
if __name__ == '__main__':
    downloader = core.SubHDDownloader()
    t = downloader.search('Person of Interest', False)
    print t
