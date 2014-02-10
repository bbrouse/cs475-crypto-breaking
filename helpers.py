
import sys
import binascii
from itertools import izip


def print_xor_files(filename1, filename2):
    file1 = open(filename1)
    file2 = open(filename2)
    output = ""

    for line1, line2 in izip(file1, file2):
        xor = xor_hex(line1.strip()[2:], line2.strip()[2:])
        if len(xor) == 1:
            xor = '0' + xor
        output += binascii.unhexlify(xor)

    print output


def xor_hex(a, b):
    result = int(a, 16) ^ int(b, 16)
    return '{:x}'.format(result)


def print_from_file(filename):
    file = open(filename)
    output = ""

    for line in file:
        hex_string = line[2:].strip()
        if len(hex_string) == 1:
            hex_string = '0' + hex_string
        output += binascii.unhexlify(hex_string)

    print output

if __name__ == "__main__":
    #print_from_file(sys.argv[1])
    print_xor_files(sys.argv[1], sys.argv[2])
