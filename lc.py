import binascii

filename = 'C:\\Users\Trevor\Google Drive\School\\2017 Spring\\Computer Organization\\Lab 2\\Memory Contents Lab 1.txt'
memory_locations = dict()


class Line:
    address, mem_bin, mem_hex, ascii, instruction, description = [None] * 5

    def __init__(self, m_address, m_contents_bin, m_contents_hex):
        self.address = m_address
        self.mem_bin = m_contents_bin
        self.mem_hex = m_contents_hex
        
        if m_contents_bin.startswith('0001') and m_contents_bin[10:11] == '0':
            self.instruction = 'ADD+'
        elif m_contents_bin.startswith('0001') and m_contents_bin[10:11] == '1':
            self.instruction = 'ADD+ (2)'
            print('Destination Register: ' + ' ' + get_bits(11, 9, m_contents_bin))
        elif m_contents_bin.startswith('0101') and m_contents_bin[10:11] == '0':
            self.instruction = 'AND+'
        elif m_contents_bin.startswith('0101') and m_contents_bin[10:11] == '1':
            self.instruction = 'AND+ (2)'
        elif m_contents_bin.startswith('0000'):
            self.instruction = 'BR'
        elif m_contents_bin.startswith('1100'):
            self.instruction = 'JMP'
        elif m_contents_bin.startswith('0100'):
            self.instruction = 'JSR'
        elif m_contents_bin.startswith('0100'):
            self.instruction = 'JSRR'
        elif m_contents_bin.startswith('0010'):
            self.instruction = 'LD+'
        elif m_contents_bin.startswith('1010'):
            self.instruction = 'LDI+'
        elif m_contents_bin.startswith('0110'):
            self.instruction = 'LDR+'
        elif m_contents_bin.startswith('1110'):
            self.instruction = 'LEA+'
        elif m_contents_bin.startswith('1001'):
            self.instruction = 'NOT+'
        elif m_contents_bin.startswith('1100'):
            self.instruction = 'RET'
        elif m_contents_bin.startswith('1000'):
            self.instruction = 'RTI'
        elif m_contents_bin.startswith('0011'):
            self.instruction = 'ST'
        elif m_contents_bin.startswith('1011'):
            self.instruction = 'STI'
        elif m_contents_bin.startswith('0111'):
            self.instruction = 'STR'
        elif m_contents_bin.startswith('1111'):
            self.instruction = 'TRAP'
        else:
            print('other')

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
