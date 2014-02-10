
import sys
import binascii
from itertools import izip
import time


class bcolors:
    #Used for printing colors in terminal
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def print_crib_drag(filename1, filename2, crib=" the "):
    file1 = open(filename1)
    file2 = open(filename2)
    cipher_xor = []

    for line1, line2 in izip(file1, file2):
        xor = xor_hex(line1.strip()[2:], line2.strip()[2:])

        if len(xor) == 1:
            xor = '0' + xor
        cipher_xor.append(xor)

    print cipher_xor
    print range(0, len(cipher_xor)-len(crib))

    output = " "
    for position in range(0, len(cipher_xor)-len(crib)):
        time.sleep(1)
        output = bcolors.OKGREEN
        for crib_letter in crib:
            cipher_hex = cipher_xor[position]
            crib_hex = crib_letter.encode("hex")
            final_hex = xor_hex(cipher_hex, crib_hex)
            final_hex = '0' + final_hex if len(final_hex) == 1 else final_hex
            output += binascii.unhexlify(final_hex)
        output += bcolors.ENDC
        print output


def print_xor_files(filename1, filename2):
    file1 = open(filename1)
    file2 = open(filename2)
    output = ""

    for line1, line2 in izip(file1, file2):
        xor = xor_hex(line1.strip()[2:], line2.strip()[2:])

        # if xor is zero, initial values were equal before padding
        if(xor == '0'):
            output += bcolors.OKGREEN
            xor = line1.strip()[2:]

        if len(xor) == 1:
            xor = '0' + xor
        output += binascii.unhexlify(xor) + bcolors.ENDC

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
    #print_xor_files(sys.argv[1], sys.argv[2])
    print_crib_drag(sys.argv[1], sys.argv[2])
