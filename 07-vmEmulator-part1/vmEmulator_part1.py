import sys
import os


# Parser

def check_command_type(type):
    return {
        'push': 'C_PUSH',
        'pop': 'C_POP',
        'add': 'C_ARITHMETIC',
        'sub': 'C_ARITHMETIC',
        'neg': 'C_ARITHMETIC',
        'eq': 'C_ARITHMETIC',
        'gt': 'C_ARITHMETIC',
        'lt': 'C_ARITHMETIC',
        'and': 'C_ARITHMETIC',
        'or': 'C_ARITHMETIC',
        'not': 'C_ARITHMETIC'
    }[type]


def parse_commande(command):
    split_command = command.split(' ')[0]
    type = check_command_type(split_command)
    arg1 = 'null'
    arg2 = 'null'
    if type == 'C_PUSH' or type == 'C_POP':
        arg1 = command.split(' ')[1]
        arg2 = command.split(' ')[2]
    yield split_command, arg1, arg2


# CodeWriter:
jmp_counter = 0
segments = {
    'argument': 'ARG',
    'local': 'LCL',
    'that': 'THAT',
    'this': 'THIS'
}


def push_to_stack():
    return ('@SP\n'
            + 'A=M\n'
            + 'M=D\n'
            + '@SP\n'
            + 'M=M+1\n')


def load_from_stack():
    return ('@SP\n'
            + 'AM=M-1\n'
            + 'D=M\n'
            + 'M=0\n')


def push(file_name, arg1, arg2):
    if arg1 == 'constant':
        return ('//push constant ' + arg2 + '\n'
                + '@' + arg2 + '\n'
                + 'D=A\n'
                + push_to_stack())
    elif arg1 in ['local', 'argument', 'this', 'that']:
        segment = segments[arg1]
        return ('//push ' + arg1 + arg2 + '\n'
                + '@' + arg2 + '\n'
                + 'D=A\n'
                + '@' + segment + '\n'
                + 'A=M+D\n'
                + 'D=M\n'
                + push_to_stack())
    elif arg1 == 'temp':
        index = 5 + int(arg2)
        return ('//push ' + arg1 + arg2 + '\n'
                + '@' + str(index) + '\n'
                + 'D=M\n'
                + push_to_stack())
    elif arg1 == 'static':
        return ('//push ' + arg1 + arg2 + '\n'
                + '@' + file_name + '.' + arg2 + '\n'
                + 'D=M\n'
                + push_to_stack())
    elif arg1 == 'pointer':
        index = 3 + int(arg2)
        return ('//push ' + arg1 + arg2 + '\n'
                                          '@' + str(index) + '\n'
                + 'D=M\n'
                + push_to_stack())


def pop(file_name, arg1, arg2):
    if arg1 in ['local', 'argument', 'this', 'that']:
        segment = segments[arg1]
        return ('//pop to ' + arg1 + arg2 + '\n'
                + '@' + arg2 + '\n'
                + 'D=A\n'
                + '@' + segment + '\n'
                + 'D=D+M\n'
                + '@R13\n'
                + 'M=D\n'
                + load_from_stack()
                + '@R13\n'
                + 'A=M\n'
                + 'M=D\n')
    elif arg1 == 'temp':
        index = 5 + int(arg2)
        return ('//pop to ' + arg1 + arg2 + '\n'
                + load_from_stack()
                + '@' + str(index) + '\n'
                + 'M=D\n')
    elif arg1 == 'static':
        return ('//pop to ' + arg1 + arg2 + '\n'
                + load_from_stack()
                + '@' + file_name + '.' + arg2 + '\n'
                + 'M=D\n')
    elif arg1 == 'pointer':
        index = 3 + int(arg2)
        return ('//pop to ' + arg1 + arg2 + '\n'
                + load_from_stack()
                + '@' + str(index) + '\n'
                + 'M=D\n')


def pop_two_elements_for_comp():
    return (load_from_stack()
            + '@SP\n'
            + 'A=M-1\n')


def pop_one_element_for_comp():
    return ('@SP\n'
            + 'A=M-1\n')


def eq_gt_lt(jmp_type):
    global jmp_counter
    return (pop_two_elements_for_comp()
            + 'D=M-D\n'
            + '@FALSE' + str(jmp_counter) + '\n'
            + 'D;' + jmp_type + '\n'
            + '@SP\n'
            + 'A=M-1\n'
            + 'M=-1\n'
            + '@CONTINUE' + str(jmp_counter) + '\n'
            + '0;JMP\n'
            + '(FALSE' + str(jmp_counter) + ')\n'
            + '@SP\n'
            + 'A=M-1\n'
            + 'M=0\n'
            + '(CONTINUE' + str(jmp_counter) + ')\n')


def arithmetic(command):
    global jmp_counter
    if command == 'add':
        return (pop_two_elements_for_comp()
                + 'M=M+D\n')
    elif command == 'sub':
        return (pop_two_elements_for_comp()
                + 'M=M-D\n')
    elif command == 'neg':
        return (pop_one_element_for_comp()
                + 'M=-M\n')
    elif command == 'eq':
        to_write = eq_gt_lt('JNE')
        jmp_counter += 1
        return to_write
    elif command == 'gt':
        to_write = eq_gt_lt('JLE')
        jmp_counter += 1
        return to_write
    elif command == 'lt':
        to_write = eq_gt_lt('JGE')
        jmp_counter += 1
        return to_write
    elif command == 'and':
        return (pop_two_elements_for_comp()
                + 'M=M&D\n')
    elif command == 'or':
        return (pop_two_elements_for_comp()
                + 'M=M|D\n')
    elif command == 'not':
        return (pop_one_element_for_comp()
                + 'M=!M\n')


# Main
vm_file_name = os.path.abspath(sys.argv[1])

vm_files = [vm_file_name]
if '.vm' not in vm_file_name: # that's mean it's a directory
    # create list of the files in the directory
    files = os.listdir(vm_file_name)
    vm_files = [os.path.join(vm_file_name, f) for f in files if os.path.join(vm_file_name, f).split('.')[1] == 'vm']
    file_or_dir_name = os.path.join(vm_file_name, vm_file_name.split('/')[-1]) + '.asm'

else:
    file_or_dir_name = vm_file_name.replace('.vm', '.asm')


output_file = open(file_or_dir_name, 'w')

for file in vm_files:
    vm_file = open(file, 'r')
    file_name = vm_file_name.split('.vm')[0]

    lines = vm_file.readlines()
    for line in lines:
        line = line.rstrip('\n')
        line = line.split('/')[0]  # remove comments
        if line:
            parser_commands = parse_commande(line)
            file_name = file_name.split('/')[-1]
            for command, arg1, arg2 in parser_commands:
                type = check_command_type(command)
                if type == 'C_PUSH':
                    output_file.write(push(file_name, arg1, arg2))
                elif type == 'C_POP':
                    output_file.write(pop(file_name, arg1, arg2))
                elif type == 'C_ARITHMETIC':
                    output_file.write(arithmetic(command))
    vm_file.close()
output_file.close()
