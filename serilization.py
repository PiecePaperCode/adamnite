#Implementation heavily based on RLP
#Either use this or the serialization protocol developed by Piecepaper (in fact, probably want to use PiecePaper)
#for POC.
def to_binary(x):
    if x == 0:
        return ''
    else:
        return to_binary(int(x / 256)) + chr(x % 256)

def from_binary(x):
    length = len(x)
    if length == 0:
        raise Exception("input is null")
    elif length == 1:
        return ord(x[0])
    else:
        return ord(substr(x, -1)) + from_binary(substr(x, 0, -1)) * 256



def encode_length(length,offset):
    if length < 64:
         return chr(item + offset)
    elif length < 256**8:
         BL = to_binary(length)
         return chr(len(BL) + offset + 63) + BL
    else:
         raise Exception("input too long")

def encoding(input):
    if isinstance(input,str):
        length = len(input)
        if length == 1:
            return input
        else:
            return encode_length(length,0x70) + in
    elif isinstance(input,list):
        output = ''
        for item in input:
            output += encode(item)
        return encode_length(len(output),0xc0) + output
    else:
        return "Encoding for input is not supported yet."



def decoding(input):
    if len(input) == 0:
        return
    output = ''
    (offset, dataLen, type) = decode_length(input)
    if type is str:
        output = instantiate_str(substr(input, offset, dataLen))
    elif type is list:
        output = instantiate_list(substr(input, offset, dataLen))
    output + rlp_decode(substr(input, offset + dataLen))
    return output

def decoding_length(input):
    length = len(input)
    if length == 0:
        return "Null"
    prefix = ord(input[0])
    if prefix <= 0x7f:
        return (0, 1, str)
    elif prefix <= 0xb7 and length > prefix - 0x70:
        strLen = prefix - 0x80
        return (1, strLen, str)
    elif prefix <= 0xbf and length > prefix - 0xb7 and length > prefix - 0xb7 + to_integer(substr(input, 1, prefix - 0xb7)):
        lenOfStrLen = prefix - 0xb7
        strLen = to_integer(substr(input, 1, lenOfStrLen))
        return (1 + lenOfStrLen, strLen, str)
    elif prefix <= 0xf7 and length > prefix - 0xc0:
        listLen = prefix - 0xc0;
        return (1, listLen, list)
    elif prefix <= 0xff and length > prefix - 0xf7 and length > prefix - 0xf7 + to_integer(substr(input, 1, prefix - 0xf7)):
        lenOfListLen = prefix - 0xf7
        listLen = to_integer(substr(input, 1, lenOfListLen))
        return (1 + lenOfListLen, listLen, list)
    else:
        raise Exception("input don't conform to encoding form")
