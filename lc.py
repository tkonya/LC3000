import binascii

filename = 'C:\\Users\Trevor\Google Drive\School\\2017 Spring\\Computer Organization\\Lab 2\\Memory Contents Lab 1.txt'
memory_locations = dict()

class Line:
    address, mem_bin, mem_hex, ascii, instruction, description, dr1, sr1, sr2, imm5 = [None] * 10
    n, z, p = [0, 0, 0]

    def describe_contents(self):
        print('Address:', self.address, '\tMemory Binary:', self.mem_bin, '\tMemory Hex:', self.mem_hex,
              '\tInstruction:', self.instruction)
        print(str(self.description) + '\n')

    def __init__(self, m_address, m_contents_bin, m_contents_hex):
        self.address = m_address
        self.mem_bin = m_contents_bin
        self.mem_hex = m_contents_hex
        
        if m_contents_bin.startswith('0001'):
            self.instruction = 'ADD+'
            self.dr1 = int(self.mem_bin[4:7], 2)
            self.sr1 = int(self.mem_bin[7:10], 2)
            if m_contents_bin[10:11] == '0':
                self.sr2 = int(self.mem_bin[13:], 2)
                self.description = 'Add the contents of R' + str(self.sr1) + ' and R' + str(self.sr2) + \
                                   ' together and put the result in R' + str(self.dr1)
            else:
                self.imm5 = int(self.mem_bin[11:], 2)
                self.description = 'Add the contents of R' + str(self.sr1) + ' and ' + str(self.imm5) + \
                                   ' together and put the result in R' + str(self.dr1)

        elif m_contents_bin.startswith('0101'):
            self.instruction = 'AND+ (Bitwise Logical And)'
            self.dr1 = int(self.mem_bin[4:7], 2)
            self.sr1 = int(self.mem_bin[7:10], 2)
            if m_contents_bin[10:11] == '0':
                self.sr2 = int(self.mem_bin[13:], 2)
                self.description = 'Perform AND operation on R' + str(self.sr1) + ' and R' + str(self.sr2) + ', and store the result in R' + str(self.dr1)
            else:
                self.imm5 = int(self.mem_bin[11:], 2)
                self.description = 'Perform AND operation on R' + str(self.sr1) + ' and ' + str(self.imm5) + ', and store the result in R' + str(self.dr1)

        elif m_contents_bin.startswith('0000'):
            n = int(self.mem_bin[4:5], 2)
            z = int(self.mem_bin[5:6], 2)
            p = int(self.mem_bin[6:7], 2)

            if n == 0 and z == 0 and p == 0:
                self.instruction = 'NOP'
                self.description = 'No operation'
            else:
                self.instruction = 'BR'
                self.description = 'Checks if the condition code is'
                if n == 1:
                    self.description += ' negative'
                    self.instruction += 'N'
                    if z == 1:
                        self.description += ' or zero'
                        self.instruction += 'Z'
                    elif p == 1:
                        self.description += ' or positive'
                        self.instruction += 'P'
                elif z == 1:
                    self.description += ' zero'
                    self.instruction += 'Z'
                    if p == 1:
                        self.description += ' or positive'
                        self.instruction += 'P'
                elif p == 1:
                    self.description += ' positive'
                    self.instruction += 'P'
                self.description += ' and if so, go to PC plus decimal ' + str(int(self.mem_bin[7:], 2))
                self.instruction += ' (Conditional Branch)'

        elif m_contents_bin.startswith('1100'):
            if int(self.mem_bin[7:10]) == 111:
                self.instruction = 'RET (Return from Subroutine)'
            else:
                self.instruction = 'JMP (Jump)'
            self.description = 'Go to the memory location stored in R' + str(int(self.mem_bin[7:10], 2))

        elif m_contents_bin.startswith('0100'):
            self.description = 'Put the incremented PC into R7 in order to return to this line later, '
            if self.mem_bin[4:5] == '1':
                self.instruction = 'JSR (Jump to Subroutine)'
                self.description += 'then jump to PC plus decimal ' + str(int(self.mem_bin[5:], 2))
            else:
                self.instruction = 'JSRR (Jump to Subroutine)'
                self.description += 'then jump to the memory location stored in R' + str(int(self.mem_bin[7:10], 2))
        elif m_contents_bin.startswith('0010'):
            self.instruction = 'LD+ (Load)'
            self.description = 'Add PC plus decimal ' + str(int(self.mem_bin[7:], 2)) + '. Load the contents of that memory location into R' + str(int(self.mem_bin[4:7], 2))
        elif m_contents_bin.startswith('1010'):
            self.instruction = 'LDI+ (Load Indirect)'
            self.description = 'Add PC plus decimal ' + str(int(self.mem_bin[7:], 2)) + ' to get the first location. Look at the first location contents to get the second location, then load the contents of the second location into R' + str(int(self.mem_bin[4:7], 2))
        elif m_contents_bin.startswith('0110'):
            self.instruction = 'LDR+ (Load Base + offset)'
            self.description = 'Calculate address by adding decimal ' + str(int(self.mem_bin[10:], 2)) + ' to the contents of R' + str(int(self.mem_bin[7:10], 2)) + '. Load the contents of memory at that location into R' + str(int(self.mem_bin[4:7], 2))
        elif m_contents_bin.startswith('1110'):
            self.instruction = 'LEA+ (Load Effective Address)'
            self.description = 'Add PC to decimal ' + str(int(self.mem_bin[7:])) + ' and loading that address into R' + str(int(self.mem_bin[4:7], 2)) + '. CC is set based on whether the value loaded is negative, zero, or positive'
        elif m_contents_bin.startswith('1001'):
            self.instruction = 'NOT+ (Bit+Wise Complement)'
            self.description = 'Store the bit-wise complement of R' + str(int(self.mem_bin[7:10], 2)) + ' into R' + str(int(self.mem_bin[4:7], 2)) + '. CC is set based on whether the value produced, as a 2s complement, is negative, zero or positive'
        elif m_contents_bin.startswith('1000'):
            self.instruction = 'RTI (Return from Interrupt)'
            self.description = 'If the processor is running in Supervisor mode, the top two elements on the Supervisor Stack are popped and loaded into PC, PSR. If the processor is running in User mode, a privilege mode violation exception occurs.'
        elif m_contents_bin.startswith('0011'):
            self.instruction = 'ST (Store)'
            self.description = 'The contents of R' + str(int(self.mem_bin[7:10], 2)) + ' are stored in memory location PC plus decimal ' + str(int(self.mem_bin[7:], 2)) + '.'
        elif m_contents_bin.startswith('1011'):
            self.instruction = 'STI (Store Indirect)'
            self.description = 'Add PC to decimal ' + str(int(self.mem_bin[7:], 2)) + ' to get address 1. The contents of address 1 are address 2. Load address 2 contents into R' + str(int(self.mem_bin[4:7], 2)) + '.'
        elif m_contents_bin.startswith('0111'):
            self.instruction = 'STR (Store Base + offset)'
            self.description = 'Get address by adding decimal ' + str(int(self.mem_bin[10:], 2)) + ' to the contents of R' + str(int(self.mem_bin[7:10], 2)) + '. Load the contents of ' + str(int(self.mem_bin[4:7], 2)) + ' into that address.'
        elif m_contents_bin.startswith('1111'):
            self.instruction = 'TRAP (System Call)'
            self.description = 'Load R7 with the incremented PC. Go to the memory location specified in the contents of memory location ' + str(int(self.mem_bin[8:], 2))
        else:
            print('other ', self.mem_bin)

        self.describe_contents()



# def get_bits(start_position, end_position, binary):
#     """Get the bits based on the bit position number, given the they are numbered backwards in the documentation"""
#     binary = '1234567890123456'
#     actual_start = abs(start_position - 15)
#     actual_end = abs(end_position - 15) + 1
#     slice = binary[actual_start:actual_end]
#     print('from ', binary, ' asked for binary at positions ', start_position, '-', end_position, ' got: ', slice)
#     return slice

# def get_bits(start_position, end_position, binary):
#     reversed_binary = binary[::-1]
#     if start_position == end_position:
#         end_position += 1
#     slice = reversed_binary[start_position:end_position]
#     return slice[::-1]

# def describe_line(binary):
#     destination_register = ''
#     if binary.startswith('0001') and binary[10:11] == '0':
#         print(binary + ' ' + 'ADD+')
#     elif binary.startswith('0001') and binary[10:11] == '1':
#         print(binary + ' ' + 'ADD+(2)')
#         print('Destination Register: ' + ' ' + get_bits(11, 9, binary))
#     elif binary.startswith('0101') and binary[10:11] == '0':
#         print(binary + ' ' + 'AND+')
#     elif binary.startswith('0101') and binary[10:11] == '1':
#         print(binary + ' ' + 'AND+(2)')
#     elif binary.startswith('0000'):
#         print(binary + ' ' + 'BR')
#     elif binary.startswith('1100'):
#         print(binary + ' ' + 'JMP')
#     elif binary.startswith('0100'):
#         print(binary + ' ' + 'JSR')
#     elif binary.startswith('0100'):
#         print(binary + ' ' + 'JSRR')
#     elif binary.startswith('0010'):
#         print(binary + ' ' + 'LD+')
#     elif binary.startswith('1010'):
#         print(binary + ' ' + 'LDI+')
#     elif binary.startswith('0110'):
#         print(binary + ' ' + 'LDR+')
#     elif binary.startswith('1110'):
#         print(binary + ' ' + 'LEA+')
#     elif binary.startswith('1001'):
#         print(binary + ' ' + 'NOT+')
#     elif binary.startswith('1100'):
#         print(binary + ' ' + 'RET')
#     elif binary.startswith('1000'):
#         print(binary + ' ' + 'RTI')
#     elif binary.startswith('0011'):
#         print(binary + ' ' + 'ST')
#     elif binary.startswith('1011'):
#         print(binary + ' ' + 'STI')
#     elif binary.startswith('0111'):
#         print(binary + ' ' + 'STR')
#     elif binary.startswith('1111'):
#         print(binary + ' ' + 'TRAP')
#     else:
#         print('other')
#
#     print('\n')


with open(filename) as f:
    for line in f:
        if line[0:1] is 'x':
            split_out = line.split(' ')
            if split_out[2] != '0000000000000000':
                memory_locations[split_out[0]] = Line(split_out[0], split_out[2], split_out[4])
                # print(split_out[0])
                # describe_line(split_out[2])
