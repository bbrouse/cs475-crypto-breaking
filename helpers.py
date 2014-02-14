
import sys
import binascii
from itertools import izip
import time
from sets import Set


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


def get_order_stats():
    stat_file = open("second-order-stats")
    statistics = {}
    alphabet = "abcdefghijklmnopqrstuvwxyz "
    for line in stat_file:
        values = line.split()
        values[0] = values[0] if values[0] != "SPACE" else " "
        statistics[values[0]] = {}
        alphabet_pos = 0
        for value in values[1:]:
            statistics[values[0]][alphabet[alphabet_pos]] = float(value)
            alphabet_pos += 1
    return statistics


def is_valid_in_second_order(letters, statistics):
    for pos, letter in enumerate(letters):
        letter = str.lower(letter)
        try:
            if not statistics[letter][str.lower(letters[pos+1])] > 0.001:
                return False
        except IndexError:
            break
        except KeyError:
            pass
    return True


def get_cribs():
    cribs = []

    crib_file = open("/usr/share/dict/connectives")
    formatting = " {} "
    for line in crib_file:
        cribs.append(formatting.format(line.strip('\n')))

    crib_file = open("cribs")
    formatting = "{}"
    for line in crib_file:
        cribs.append(formatting.format(line.strip('\n')))

    return sorted(Set(cribs))


def print_crib_drag(filename1, filename2, crib=""):
    file1 = open(filename1)
    file2 = open(filename2)
    cipher_xor = []
    statistics = get_order_stats()
    matches = []

    message1 = ["_"]*128
    message2 = ["_"]*128

    acceptable_chars = range(65, 91) + range(97, 123) + [46, 32]

    print "Gathering cribs"
    if crib:
        cribs = [crib]
    else:
        cribs = get_cribs()

    for crib in cribs:
        for line1, line2 in izip(file1, file2):
            xor = xor_hex(line1.strip()[2:], line2.strip()[2:])

            if len(xor) == 1:
                xor = '0' + xor
            cipher_xor.append(xor)

        for position in range(0, len(cipher_xor)-len(crib)):
            output = ""
            for crib_letter in crib:
                cipher_hex = cipher_xor[position]
                crib_hex = binascii.hexlify(crib_letter)
                final_hex = xor_hex(cipher_hex, crib_hex)
                final_hex = '0' + final_hex if len(final_hex) == 1 else final_hex
                output += binascii.unhexlify(final_hex)
                position += 1

            is_text = True
            is_valid = False
            for letter in output:
                if not ord(letter) in acceptable_chars:
                    is_text = False
                    break

            if is_text:
                is_valid = is_valid_in_second_order(output, statistics)

            if is_text and is_valid:
                matches.append([position, crib, output])

            '''
            if is_text and is_valid:
                message1[position:position + len(crib)] = crib
                message2[position:position + len(crib)] = output
            '''
        print "Processed crib dragging for: {}".format(crib)

    print "Done.  Printing matches"
    time.sleep(1.5)
    #print "Message 1: {}\n\nMessage 2: {}\n\n".format("".join(message1), "".join(message2))
    for match in matches:
        print match


def print_xor_files(filename1, filename2, pretty_print=False, output_hex=False):
    file1 = open(filename1)
    file2 = open(filename2)
    output = ""

    position = 0
    for line1, line2 in izip(file1, file2):
        xor = xor_hex(line1.strip()[2:], line2.strip()[2:])

        # if xor is zero, initial values were equal before padding
        if(xor == '0'):
            output += bcolors.OKBLUE
            xor = line1.strip()[2:]

        if len(xor) == 1:
            xor = '0' + xor

        if pretty_print:
            if output_hex:
                output += "{}: {}\n".format(position, xor + bcolors.ENDC)
            else:
                output += "{}: {}\n".format(position, binascii.unhexlify(xor) + bcolors.ENDC)
        else:
            output += binascii.unhexlify(xor) + bcolors.ENDC

        position += 1

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
    print_crib_drag(sys.argv[1], sys.argv[2], sys.argv[3])
