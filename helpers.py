
import sys
import binascii


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
    print_from_file(sys.argv[1])
