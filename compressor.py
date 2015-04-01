import rarfile
import zipfile

class BaseCompressedFileHandler(object):
    def __init__(self, sub_buff, compression_class):
        self.archieve_object = compression_class(sub_buff)

    def list_info(self):
        info_list = []
        for i in self.archieve_object.infolist():
            info = {
                'size': i.file_size,
                'name': i.filename,
                'info_obj': i
            }
            info_list.append(info)
        return info_list

    def extract(self, filename):
        raw_subfile = self.archieve_object.open(filename, 'r')
        raw_sub = raw_subfile.read()
        raw_subfile.close()
        return raw_sub

    def extract_bestguess(self):
        info = self.list_info()
        candidate = max(info, key=lambda x: x['size'])
        return (candidate['name'], self.extract(candidate['name']))

class RARFileHandler(BaseCompressedFileHandler):
    def __init__(self, sub_buff):
        super(RARFileHandler, self).__init__(sub_buff, rarfile.RarFile)

class ZIPFileHandler(BaseCompressedFileHandler):
    def __init__(self, sub_buff):
        super(ZIPFileHandler, self).__init__(sub_buff, zipfile.ZipFile)
