import plyvel
import rlp#Implemenation based on PyEthereum
import hashlib
#Add reputation (socre quantifying the behavior of previous blocks)

class main_DB():
    def __init__(self,data_file):
        self.db = plyvel.DB(data_file, create_if_missing=True)
    def retrieve(self,key):
        try: return self.db.get(key)
        except: return ''
    def add(self,key,value):
        return self.db.put(key,value)
    def delete(self,key):
        return self.db.delete(key)
data = {}
class tree():
    def __init__(self,data_file,root='',debug=False):
        self.root = root
        self.debug = debug
        if dbfile not in data:
            data[dbfile] = main_DB(dbfile)
        self.db = data[dbfile]

    def __encode_key(self,key):
        term = 1 if key[-1] == 16 else 0
        oddlen = (len(key) - term) % 2
        prefix = ('0' if oddlen else '')
        main = ''.join(['0123456789abcdef'[x] for x in key[:len(key)-term]])
        return chr(2 * term + oddlen) + (prefix+main).decode('hex')

    def __decode_key(self,key):
        o = ['0123456789abcdef'.find(x) for x in key[1:].encode('hex')]
        if key[0] == '\x01' or key[0] == '\x03': o = o[1:]
        if key[0] == '\x02' or key[0] == '\x03': o.append(16)
        return o
