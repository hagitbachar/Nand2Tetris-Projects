import sys


def dest_in_binary(dest):
    if dest is None:
        return '000'
    return {
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111'
    }[dest]


def comp_in_binary(comp):
    return {
        '0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000',
        '!D': '0001101',
        '!A': '0110001',
        '-D': '0001111',
        '-A': '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'D|A': '0010101',
        'M': '1110000',
        '!M': '1110001',
        '-M': '1110011',
        'M+1': '1110111',
        'M-1': '1110010',
        'D+M': '1000010',
        'D-M': '1010011',
        'M-D': '1000111',
        'D&M': '1000000',
        'D|M': '1010101',
        'D<<': '101010',
        'A<<': '101011',
        'M<<': '101110',
        'D>>': '101001',
        'A>>': '101000',
        'M>>': '101100'
    }[comp]


def jmp_in_binary(jmp):
    if jmp is None:
        return '000'
    return {
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }[jmp]


# pre-defined symbols, we will add more symbols that appear in the asm file
all_symbols = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R1O': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4
}

address_to_store = 16

def parseAInstruction(instruction):
    number = instruction[1:]

    if number.isdigit():
        number = bin(int(number)).split('0b')[1]  # convert to binary
        num_of_zero_to_add = 15 - len(number)
        number = '0' * (num_of_zero_to_add + 1) + number  # add zeros to get a 16-bit number, +1 for the 0 opcode
    else:
        if all_symbols.__contains__(number):
            number = all_symbols[number]  # take the address from the symbol table
        else:
            global address_to_store
            all_symbols[number] = address_to_store
            number = address_to_store
            address_to_store += 1

        number = bin(int(number)).split('0b')[1]  # convert to binary
        num_of_zero_to_add = 15 - len(number)
        number = '0' * (num_of_zero_to_add + 1) + number  # add zeros to get a 16-bit number, +1 for the 0 opcode
    return number


def parseCInstruction(instruction):
    dest = None
    jmp = None

    comp = instruction
    if instruction.__contains__("="):
        dest = instruction.split('=')[0]
        comp = instruction.split('=')[1]

    if instruction.__contains__(";"):
        jmp = comp.split(';')[1]
        comp = comp.split(';')[0]

    dest = dest_in_binary(dest)
    comp = comp_in_binary(comp)
    jmp = jmp_in_binary(jmp)
    return '111' + comp + dest + jmp


def parser(line):
    # check if A-instruction or C-instruction
    if line[0] == '@':
        binary_instruction = parseAInstruction(line)
    else:
        binary_instruction = parseCInstruction(line)

    return binary_instruction


instruction = []

asm_file_name = sys.argv[1]
asm_file = open(asm_file_name, 'r')

file_name = asm_file_name.split('.asm')[0]
file_name = file_name + ".hack"
output_file = open(file_name, 'w')

lines = asm_file.readlines()

# first pass- add the label symbol in the file to the symbols table
unimportent_row = 1
num_row = 0
for line in lines:
    num_row += 1
    line = line.rstrip('\n')
    line = line.split('/')[0]  # remove comments
    line = line.replace(' ', '')  # remove spaces
    if line:
        instruction.append(line)
        if line[0] == '(':
            line = line.split('(')[1]
            line = line.split(')')[0]
            all_symbols[line] = num_row - unimportent_row
            unimportent_row += 1
    else:
        unimportent_row += 1

# second pass- parse the instruction and convert to binary (and add variable symbols to the symbols table)
row = 0
for line in instruction:
    if line[0] == '(':
        continue
    output_file.write(str(parser(line)) + '\r\n')

asm_file.close()
output_file.close()


