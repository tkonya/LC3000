filename = 'C:\\Users\Trevor\\Google Drive\\School\\2017 Spring\\Computer Organization\\Lab 2\\Memory Contents Lab 1.txt'
memory_locations = dict()
ascii_table = {
    '00100000': '(space)',
    '00001101': '(return)',
    '00110000': '0',
    '00110001': '1',
    '00110010': '2',
    '00110011': '3',
    '00110100': '4',
    '00110101': '5',
    '00110110': '6',
    '00110111': '7',
    '00111000': '8',
    '00111001': '9',
    '01000001': 'A',
    '01000010': 'B',
    '01000011': 'C',
    '01000100': 'D',
    '01000101': 'E',
    '01000110': 'F',
    '01000111': 'G',
    '01001000': 'H',
    '01001001': 'I',
    '01001010': 'J',
    '01001011': 'K',
    '01001100': 'L',
    '01001101': 'M',
    '01001110': 'N',
    '01001111': 'O',
    '01010000': 'P',
    '01010001': 'Q',
    '01010010': 'R',
    '01010011': 'S',
    '01010100': 'T',
    '01010101': 'U',
    '01010110': 'V',
    '01010111': 'W',
    '01011000': 'X',
    '01011001': 'Y',
    '01011010': 'Z',
    '01100001': 'a',
    '01100010': 'b',
    '01100011': 'c',
    '01100100': 'd',
    '01100101': 'e',
    '01100110': 'f',
    '01100111': 'g',
    '01101000': 'h',
    '01101001': 'i',
    '01101010': 'j',
    '01101011': 'k',
    '01101100': 'l',
    '01101101': 'm',
    '01101110': 'n',
    '01101111': 'o',
    '01110000': 'p',
    '01110001': 'q',
    '01110010': 'r',
    '01110011': 's',
    '01110100': 't',
    '01110101': 'u',
    '01110110': 'v',
    '01110111': 'w',
    '01111000': 'x',
    '01111001': 'y',
    '01111010': 'z'
}


class Line:
    address, mem_bin, mem_hex, ascii, instruction, description, dr1, sr1, sr2, imm5 = [None] * 10
    n, z, p = [0, 0, 0]
    twos_complement = 0
    ascii = ''

    @staticmethod
    def get_twos_complement(val, bits):
        if (val & (1 << (bits - 1))) != 0:
            val -= 1 << bits
        return val

    @staticmethod
    def format_hex(hex_value):
        if len(str(hex_value[2:])) == 1:
            return 'x000' + str(hex_value[2:]).upper()
        elif len(str(hex_value[2:])) == 2:
            return 'x00' + str(hex_value[2:]).upper()
        elif len(str(hex_value[2:])) == 3:
            return 'x0' + str(hex_value[2:]).upper()
        else:
            return 'x' + str(hex_value[2:]).upper()

    def describe_contents(self):

        ascii_section = ''
        if self.instruction == 'NOP':
            ascii_section = '\t\t\t\t\tASCII: ' + self.ascii

        print(self.address,
              '  ------------------------------------------------------------------------------------------',
              '\n\t\tMem Binary:', self.mem_bin,
              '\t\tMem Hex:', self.mem_hex,
              '\t\tInstruction:', self.instruction,
              '\n\t\t2s Complement:', self.twos_complement,
              ascii_section,
              '\n\t\t' + str(self.description), '\n\n')

    def __init__(self, m_address, m_contents_bin, m_contents_hex):
        self.address = m_address
        self.mem_bin = m_contents_bin
        self.mem_hex = m_contents_hex
        self.twos_complement = self.get_twos_complement(int(self.mem_bin, 2), 16)
        self.ascii = ascii_table.get(m_contents_bin[8:], 'N/A')

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
                self.description = 'Perform AND operation on R' + str(self.sr1) + ' and R' + str(
                    self.sr2) + ', and store the result in R' + str(self.dr1)
            else:
                self.imm5 = int(self.mem_bin[11:], 2)
                self.description = 'Perform AND operation on R' + str(self.sr1) + ' and ' + str(
                    self.imm5) + ', and store the result in R' + str(self.dr1)

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
            self.description = 'Add PC plus decimal ' + str(
                int(self.mem_bin[7:], 2)) + '. Load the contents of that memory location into R' + str(
                int(self.mem_bin[4:7], 2))
        elif m_contents_bin.startswith('1010'):
            self.instruction = 'LDI+ (Load Indirect)'
            self.description = 'Add PC plus decimal ' + str(int(self.mem_bin[7:],
                                                                2)) + ' to get the first location. Look at the first location contents to get the second location, then load the contents of the second location into R' + str(
                int(self.mem_bin[4:7], 2))
        elif m_contents_bin.startswith('0110'):
            self.instruction = 'LDR+ (Load Base + offset)'
            self.description = 'Calculate address by adding decimal ' + str(
                int(self.mem_bin[10:], 2)) + ' to the contents of R' + str(
                int(self.mem_bin[7:10], 2)) + '. Load the contents of memory at that location into R' + str(
                int(self.mem_bin[4:7], 2))
        elif m_contents_bin.startswith('1110'):
            self.instruction = 'LEA+ (Load Effective Address)'
            self.description = 'Add ' + self.format_hex(hex(int(self.mem_bin[7:], 2))) + \
                               ' to PC and load that address into R' + str(int(self.mem_bin[4:7], 2)) + \
                               '. CC is set based on whether the value loaded is negative, zero, or positive'
        elif m_contents_bin.startswith('1001'):
            self.instruction = 'NOT+ (Bit+Wise Complement)'
            self.description = 'Store the bit-wise complement of R' + str(int(self.mem_bin[7:10], 2)) + ' into R' + str(
                int(self.mem_bin[4:7],
                    2)) + '. CC is set based on whether the value produced, as a 2s complement, is negative, zero or positive'
        elif m_contents_bin.startswith('1000'):
            self.instruction = 'RTI (Return from Interrupt)'
            self.description = 'If the processor is running in Supervisor mode, the top two elements on the Supervisor Stack are popped and loaded into PC, PSR. If the processor is running in User mode, a privilege mode violation exception occurs.'
        elif m_contents_bin.startswith('0011'):
            self.instruction = 'ST (Store)'
            self.description = 'The contents of R' + str(
                int(self.mem_bin[7:10], 2)) + ' are stored in memory location PC plus decimal ' + str(
                int(self.mem_bin[7:], 2)) + '.'
        elif m_contents_bin.startswith('1011'):
            self.instruction = 'STI (Store Indirect)'
            self.description = 'Add PC to decimal ' + str(int(self.mem_bin[7:],
                                                              2)) + ' to get address 1. The contents of address 1 are address 2. Load address 2 contents into R' + str(
                int(self.mem_bin[4:7], 2)) + '.'
        elif m_contents_bin.startswith('0111'):
            self.instruction = 'STR (Store Base + offset)'
            self.description = 'Get address by adding decimal ' + str(
                int(self.mem_bin[10:], 2)) + ' to the contents of R' + str(
                int(self.mem_bin[7:10], 2)) + '. Load the contents of ' + str(
                int(self.mem_bin[4:7], 2)) + ' into that address.'
        elif m_contents_bin.startswith('1111'):
            self.instruction = 'TRAP (System Call)'
            self.description = 'Load R7 with the incremented PC. Go to the memory location specified in the contents ' \
                               'of memory location ' + self.format_hex(hex(int(self.mem_bin[8:], 2)))
        else:
            print('other ', self.mem_bin)

        self.describe_contents()


with open(filename) as f:
    for line in f:
        if line[0:1] is 'x':
            split_out = line.split(' ')
            if split_out[2] != '0000000000000000':
                memory_locations[split_out[0]] = Line(split_out[0], split_out[2], split_out[4])
                # print(split_out[0])
                # describe_line(split_out[2])
