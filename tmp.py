import tempfile

__tmp_files = {}

def mktmp():
    tmp = tempfile.NamedTemporaryFile(mode='w',encoding='utf-8')
    __tmp_files[tmp.name] = tmp
    return tmp.name

def rmtmp(file):
    __tmp_files[file].close()

def close_all():
    for x in __tmp_files:
        __tmp_files[x].close()
