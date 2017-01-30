import binascii

filename = 'C:\\Users\Trevor\Google Drive\School\\2017 Spring\\Computer Organization\\Lab 2\\Memory Contents Lab 1.txt'
memory_locations = dict()

class Line:
    memory_address = ''
    memory_contents_bin = ''
    memory_contents_hex = ''
    ascii = ''
    instruction = ''

    def __init__(self, m_address, m_contents_bin, m_contents_hex):
        self.memory_address = m_address
        self.memory_contents_bin = m_contents_bin
        self.memory_contents_hex = m_contents_hex

    def describe_contents(self):
        print('memory thing')


def get_bits(start_position, end_position, binary):
    """Get the bits based on the bit position number, given the they are numbered backwards in the documentation"""
    actual_start = abs(start_position - 15)
    actual_end = abs(end_position - 15) + 1
    return binary[actual_start:actual_end]

def describe_line(binary):
    destination_register = ''
    if binary.startswith('0001') and binary[10:11] == '0':
        print(binary + ' ' + 'ADD+')
    elif binary.startswith('0001') and binary[10:11] == '1':
        print(binary + ' ' + 'ADD+(2)')
        print('Destination Register: ' + ' ' + get_bits(11, 9, binary))
    elif binary.startswith('0101') and binary[10:11] == '0':
        print(binary + ' ' + 'AND+')
    elif binary.startswith('0101') and binary[10:11] == '1':
        print(binary + ' ' + 'AND+(2)')
    elif binary.startswith('0000'):
        print(binary + ' ' + 'BR')
    elif binary.startswith('1100'):
        print(binary + ' ' + 'JMP')
    elif binary.startswith('0100'):
        print(binary + ' ' + 'JSR')
    elif binary.startswith('0100'):
        print(binary + ' ' + 'JSRR')
    elif binary.startswith('0010'):
        print(binary + ' ' + 'LD+')
    elif binary.startswith('1010'):
        print(binary + ' ' + 'LDI+')
    elif binary.startswith('0110'):
        print(binary + ' ' + 'LDR+')
    elif binary.startswith('1110'):
        print(binary + ' ' + 'LEA+')
    elif binary.startswith('1001'):
        print(binary + ' ' + 'NOT+')
    elif binary.startswith('1100'):
        print(binary + ' ' + 'RET')
    elif binary.startswith('1000'):
        print(binary + ' ' + 'RTI')
    elif binary.startswith('0011'):
        print(binary + ' ' + 'ST')
    elif binary.startswith('1011'):
        print(binary + ' ' + 'STI')
    elif binary.startswith('0111'):
        print(binary + ' ' + 'STR')
    elif binary.startswith('1111'):
        print(binary + ' ' + 'TRAP')
    else:
        print('other')

    print('\n')


with open(filename) as f:
    for line in f:
        if line[0:1] is 'x':
            split_out = line.split(' ')
            if split_out[2] != '0000000000000000':
                memory_locations[split_out[0]] = Line(split_out[0], split_out[2])
                print(split_out[0])
                describe_line(split_out[2])
