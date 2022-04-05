import marshal
import os
import pickle
import sys
from array import array
from turtle import position
from typing import Dict
from typing import Tuple

#Jason Bachman
# In building the Huffman tree I am using nodes to represent each point on the tree as each node holds its frequency, data if it has any, 
# and pointers to its left and right children if it has any.
# I am storing all the nodes in a list which I sort and remove children everytime I add to the tree. 
# The final tree is represented by the relationship stored within the nodes.
# I build the frequencies in a dictionary by iterating over the message and updating it each time a character is found.
# The code is made by recursively traversing the tree until a leaf is found adding a 1 or 0 based on the direction it takes to the child. Once a leaf is found
# the data is stored in a dictionary with the code that was built in getting to that leaf
# Decoding is handled by taking one character at a time and checking the dictionary to see if it a valid path. If not it adds another char.
# if it is a valid path it takes the val for that key and adds it to the decrypted message before ckearing the current enigma path and pulling more characters.
# Invarients: child nodes are always smaller then their parents. 
#           : Nodes are sorted left to right.
#           : Leaf nodes have no children and store the ascii code
#           : The of nodes shrinks until the whole tree relationship is defined
#           : All nodes popped from the list have a parent
#           : While decoding the coded message is dissassembled from the front and the message is done when the coded message is empty
# 






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
    print(codec)
    for j in message:
        code += codec[j]
    
    
    return [code, codec]



    raise NotImplementedError


def get_key(val,ring):
    for key, value in ring.items():
        if val == value:
            return key


def decode(message: str, decoder_ring: Dict) -> bytes:
    """ Given the encoded string and the decoder ring, decodes the message using the Huffman decoding algorithm.

    :param message: string of 1s and 0s representing the encoded message
    :param decoder_ring: dict containing the decoder ring
    return: raw sequence of bytes that represent a decoded file
    """
    print(decoder_ring)
    print(message)
    
    enigma = ''
    byte_array = array('B')
    while len(message) > 0:
        enigma += message[0]
        message = message[1:]
        if enigma in decoder_ring.values():
            val = get_key(enigma,decoder_ring)
            byte_array.append(val)
            enigma = ''
    return byte_array    
        




    raise NotImplementedError


def compress(message: bytes) -> Tuple[array, Dict]:
    """ Given the bytes read from a file, calls encode and turns the string into an array of bytes to be written to disk.

    :param message: raw sequence of bytes from a file
    :returns: array of bytes to be written to disk
                dict containing the decoder ring
    """

    coded,ring = encode(message)
    double_coded = bytearray(coded,"ascii")
    pad = 0
    while sys.getsizeof(double_coded) % 8 != 0:
        double_coded.append(0)
        pad += 1
    ring['padding'] = pad
    return [double_coded, ring]


    raise NotImplementedError


def decompress(message: array, decoder_ring: Dict) -> bytes:
    """ Given a decoder ring and an array of bytes read from a compressed file, turns the array into a string and calls decode.

    :param message: array of bytes read in from a compressed file
    :param decoder_ring: dict containing the decoder ring
    :return: raw sequence of bytes that represent a decompressed file
    """
    

    padding = decoder_ring.get("padding")
    while padding >=1:
        message.pop()
        padding-=1

    coded = str(message, 'utf-8')
    decoded_message = decode(coded,decoder_ring)
    return decoded_message
    raise NotImplementedError


if __name__ == '__main__':
    usage = f'Usage: {sys.argv[0]} [ -c | -d | -v | -w ] infile outfile'
    if len(sys.argv) != 4:
        raise Exception(usage)

    operation = sys.argv[1]
    if operation not in {'-c', '-d', '-v', '-w'}:
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