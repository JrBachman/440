import marshal
import os
import pickle
import sys
from array import array
from typing import Dict
from typing import Tuple
from bitarray import bitarray


class Node(object):
    def __init__(self, data, freq,l,r):
        self.left = l
        self.right = r
        self.freq = freq
        self.data = data


def make_code(node, code=''):
    if node.data != None:
        return {node.data: code}
    c = dict()
    c.update(make_code(node.left, code + '0'))
    c.update(make_code(node.right, code + '1'))
    return c
    



def encode(message: bytes) -> Tuple[str, Dict]:
    """ Given the bytes read from a file, encodes the contents using the Huffman encoding algorithm.

    :param message: raw sequence of bytes from a file
    :returns: string of 1s and 0s representing the encoded message
            dict containing the decoder ring as explained in lecture and handout.
    """


    '''byte_str = message = f’{byte_str:08b}’'''
    freqs = {}
    for i in message:
        if i in freqs:
            freqs[i] += 1
        else:
            freqs[i] = 1

    freqs = sorted(freqs.items(), key=lambda x: x[1], reverse = False)
    nodes = []
    for key,val in freqs:
        nodes.append(Node(key,val,None,None))
    while len(nodes) > 1:
        nodes.sort(key=lambda x: x.freq, reverse=False)
        sum = nodes[0].freq + nodes[1].freq
        nodes.append(Node(None,sum,nodes[0],nodes[1]))
        nodes.pop(0)
        nodes.pop(0)
        
    codec = make_code(nodes[0])
    code = ''
    
    #for key,val in freqs:
    #    print(key,codec[key])
    #print(codec)
    for j in message:
        code += codec[j]
    
    
    return [code, codec]



    raise NotImplementedError


def decode(message: str, decoder_ring: Dict) -> bytes:
    """ Given the encoded string and the decoder ring, decodes the message using the Huffman decoding algorithm.

    :param message: string of 1s and 0s representing the encoded message
    :param decoder_ring: dict containing the decoder ring
    return: raw sequence of bytes that represent a decoded file
    """




    dec = bitarray(message).decode(decoder_ring)
    print(dec)
    raise NotImplementedError


def compress(message: bytes) -> Tuple[array, Dict]:
    """ Given the bytes read from a file, calls encode and turns the string into an array of bytes to be written to disk.

    :param message: raw sequence of bytes from a file
    :returns: array of bytes to be written to disk
                dict containing the decoder ring
    """
    raise NotImplementedError


def decompress(message: array, decoder_ring: Dict) -> bytes:
    """ Given a decoder ring and an array of bytes read from a compressed file, turns the array into a string and calls decode.

    :param message: array of bytes read in from a compressed file
    :param decoder_ring: dict containing the decoder ring
    :return: raw sequence of bytes that represent a decompressed file
    """
    raise NotImplementedError


if __name__ == '__main__':
    usage = f'Usage: {sys.argv[0]} [ -c | -d | -v | -w ] infile outfile'
    if len(sys.argv) != 4:
        raise Exception(usage)

    operation = sys.argv[1]
    if operation not in {'-c', '-d', '-v', 'w'}:
        raise Exception(usage)

    infile, outfile = sys.argv[2], sys.argv[3]
    if not os.path.exists(infile):
        raise FileExistsError(f'{infile} does not exist.')

    if operation in {'-c', '-v'}:
        with open(infile, 'rb') as fp:
            _message = fp.read()

        if operation == '-c':
            _message, _decoder_ring = compress(_message)
            with open(outfile, 'wb') as fp:
                marshal.dump((pickle.dumps(_decoder_ring), _message), fp)
        else:
            _message, _decoder_ring = encode(_message)
            print(_message)
            with open(outfile, 'wb') as fp:
                marshal.dump((pickle.dumps(_decoder_ring), _message), fp)

    else:
        with open(infile, 'rb') as fp:
            pickleRick, _message = marshal.load(fp)
            _decoder_ring = pickle.loads(pickleRick)

        if operation == '-d':
            bytes_message = decompress(array('B', _message), _decoder_ring)
        else:
            bytes_message = decode(_message, _decoder_ring)
        with open(outfile, 'wb') as fp:
            fp.write(bytes_message)