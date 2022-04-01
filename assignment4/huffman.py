import marshal
import os
import pickle
import sys
from array import array
from typing import Dict
from typing import Tuple

class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d

def encode(message: bytes) -> Tuple[str, Dict]:
    """ Given the bytes read from a file, encodes the contents using the Huffman encoding algorithm.

    :param message: raw sequence of bytes from a file
    :returns: string of 1s and 0s representing the encoded message
              dict containing the decoder ring as explained in lecture and handout.
    """


    '''byte_str = message = f’{byte_str:08b}’'''
    
    freq = {}
    for i in message:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    nodes = freq
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))
    huffmanCode = huffman_code_tree(nodes[0][0])

    print(' Char | Huffman code ')
    print('----------------------')
    for (char, frequency) in freq:
        print(' %-4r |%12s' % (char, huffmanCode[char]))
                       
    
    raise NotImplementedError


def decode(message: str, decoder_ring: Dict) -> bytes:
    """ Given the encoded string and the decoder ring, decodes the message using the Huffman decoding algorithm.

    :param message: string of 1s and 0s representing the encoded message
    :param decoder_ring: dict containing the decoder ring
    return: raw sequence of bytes that represent a decoded file
    """
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