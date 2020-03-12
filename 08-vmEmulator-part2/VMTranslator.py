import sys, os


def write_line(asmline, asm):
    # this method adds a line to the asm file.

    asm.write(asmline)
    asm.write("\n")


def label_dec(label_name, asm_file):
    str = "\n(" + label_name + ")"
    write_line(str, asm_file)

def goto_label(label_name, asm_file):
    str = "\n@" + label_name + "\n0; JMP"
    write_line(str, asm_file)

def if_goto_label(label_name, asm_file):
    str = "\n@SP \nM = M-1 \nA = M \nD = M \n@" + label_name + "\nD; JNE"
    write_line(str, asm_file)


def def_function(file_name, funct_name, Nvars, funct_counter, asm_file):
    #if funct_name == "Sys.init":
    #   funct_counter = call_funct(file_name, funct_name, str(0), funct_counter, asm_file)
    line = "\n(function." + funct_name + ")"
    for i in range(int(Nvars)):
        line = line + "\n@" + str(i) + "\nD = A" + "\n@LCL \nA = D + M \nM = 0"
    line = line + "\n@" + Nvars + "\nD = A \n@SP \nM = D + M"
    write_line(line, asm_file)
    return funct_counter


def call_funct(file_name, funct_name, Nargs, funct_counter, asm_file):
    line = "\n@" + file_name + "$ret." + str(funct_counter) + "\nD = A \n@SP \nM = M + 1 \nA = M - 1 \nM = D" + \
          "\n@LCL \nD = M \n@SP \nM = M + 1 \nA = M - 1 \nM = D" + \
          "\n@ARG \nD = M \n@SP \nM = M + 1 \nA = M - 1 \nM = D" + \
          "\n@THIS \nD = M \n@SP \nM = M + 1 \nA = M - 1 \nM = D" + \
          "\n@THAT \nD = M \n@SP \nM = M + 1 \nA = M - 1 \nM = D" +  \
          "\n@5 \nD = A \n@" + Nargs \
           + "\nD = D + A \n@SP \nD = M - D \n@ARG \nM = D" + \
          "\n@SP \nD = M \n@LCL \nM = D" + \
          "\n@function." + funct_name + "\n0; JMP" + \
          "\n(" + file_name + "$ret." + str(funct_counter) + ")"
    funct_counter += 1
    write_line(line, asm_file)
    return funct_counter

def funct_return(file_name, funct_counter, asm_file):
    line = "\n@5 \nD = A \n@LCL \nA = M - D \nD = M \n@R14 \nM = D" +\
           "\n@SP \nA = M - 1 \nD = M \n@ARG \nA = M \nM = D" + \
          "\n@ARG \nD = M \n@SP \nM = D + 1" + \
          "\n@LCL \nD = M \n@R13 \nM = D - 1 " +\
          "\nA = M \nD = M \n@THAT \nM = D \n@R13 \nM = M - 1" + \
          "\nA = M \nD = M \n@THIS \nM = D \n@R13 \nM = M - 1" + \
          "\nA = M \nD = M \n@ARG \nM = D \n@R13 \nM = M - 1" + \
          "\nA = M \nD = M \n@LCL \nM = D" + \
          "\n@R14 \nA = M \n0;JMP "# + "\n@LCL \nM = D \n@R13 \nM = M - 1 \n@" + "Sys" + "$ret." + str(funct_counter) + "\n0; JMP"
    write_line(line, asm_file)
    funct_counter -= 1
    return funct_counter


def add_beginning(plus_or_minus):
    # this method adds the beginning to some arithmetic or logic commands.

    str = "@SP \nM = M-1 \nA = M \nD = M \nA = A-1 \nD = " + plus_or_minus
    return str


def add_end_command(line, jmp, counter):
    # this method adds the end to some arithmetic or logic commands.

    counter = str(counter)
    line = line + "\n@TRUE" + counter + " \nD; " + jmp + " \n@SP \nA = M-1 \nM = 0 \n@AFTERTRUE" + counter + " \n" \
                                      "0; JMP \n(TRUE" + counter + ") \n@SP \n" \
                                      "A = M-1 \nM = -1 \n(AFTERTRUE" + counter + ")"
    return line


def handle_arithmetic_logic_command(command, asm, count):
    # this method gets an arithmetic or logic command and
    # adds the asm translation to the asm file.

    if command == "add":
        write_line(add_beginning("D + M") + " \nM = D", asm)
    elif command == "sub":
        write_line(add_beginning("M - D") + "\nM = D", asm)
    elif command == "neg":
        write_line("@SP \nA = M-1 \nM = -M", asm)
    elif command == "eq":
        str = add_end_command(add_beginning("M - D"), "JEQ", count)
        count += 1
        write_line(str, asm)
    elif command == "gt":
        str = add_end_command(add_beginning("M - D"), "JGT", count)
        count += 1
        write_line(str, asm)
    elif command == "lt":
        str = add_end_command(add_beginning("M - D"), "JLT", count)
        count += 1
        write_line(str, asm)
    elif command == "and":
        str = add_beginning("D & M") + " \nM = D"
        count += 1
        write_line(str, asm)
    elif command == "or":
        str = add_beginning("D | M") + " \nM = D"
        count += 1
        write_line(str, asm)
    elif command == "not":
        str = "@SP \nA = M - 1 \nM = !M"
        write_line(str, asm)
    return count


def add_ending_pop(str, i, a_or_m):
    # this method gets the specific pop command and puts it into
    # the asm format, then returns the asm line.

    new_str = str + "D = " + a_or_m + " \n@" + i + " \nD = D + A \n@R13 \nM = D \n@SP \n" \
                                                        "M = M-1 \nA = M \nD = M \n@R13 \nA = M \nM = D"
    return new_str


def add_ending_push(str, i , a_or_m, middle_part):
    # this method gets the specific "push" command and puts it into
    # the asm format, then returns the asm line.

    new_str = str + "D = " + a_or_m
    if middle_part:
        new_str = new_str + " \n@" + i + " \nA = D + A \nD = M"
    new_str = new_str + "\n@SP \nM = M+1 \nA = M-1 \nM = D"
    return new_str


def handle_push(segment, i, file_name):
    # this method gets a "push" command and returns the asm translation.

    if segment == "local":
        str = add_ending_push("@LCL \n", i, "M", True)
    elif segment == "argument":
        str = add_ending_push("@ARG \n", i, "M", True)
    elif segment == "this":
        str = add_ending_push("@THIS \n", i, "M", True)
    elif segment == "that":
        str = add_ending_push("@THAT \n", i, "M", True)
    elif segment == "temp":
        str = add_ending_push("@5 \n", i, "A", True)
    elif segment == "constant":
        str = add_ending_push("@" + i + "\n", i, "A", False)
    elif segment == "static":
        str = add_ending_push("@" + file_name + "." + i + "\n", i, "M", False)
    elif segment == "pointer":
        if i == "0":
            point = "THIS"
        if i == "1":
            point = "THAT"
        str = add_ending_push("@" + point + "\n", i, "M", False)
    return str


def handle_pop(segment, i, file_name):
    # this method gets a "pop" command and returns the asm translation.

    if segment == "local":
        str = add_ending_pop("@LCL \n", i, "M")
    elif segment == "argument":
        str = add_ending_pop("@ARG \n", i, "M")
    elif segment == "this":
        str = add_ending_pop("@THIS \n", i, "M")
    elif segment == "that":
        str = add_ending_pop("@THAT \n", i, "M")
    elif segment == "temp":
        str = add_ending_pop("@5 \n", i, "A")
    elif segment == "static":
        str = "@SP \nM = M-1 \nA = M \nD = M \n@" + file_name + "." + i + " \nM = D"
    elif segment == "pointer":
        if i == "0":
            point = "THIS"
        if i == "1":
            point = "THAT"
        str = "@SP \nM = M-1 \nA = M \nD = M \n@" + point + " \nM = D"
    return str


def handle_memory_command(command, segment, i, asm, file_name):
    # this method gets a memory command and send it
    # to be handled either as a push command or a pop command.
    # after getting the translation it adds it to the asm file.

    str = ""
    if command == "pop":
        str = handle_pop(segment, i, file_name)
        write_line(str, asm)
        return
    if command == "push":
        str = handle_push(segment, i, file_name)
        write_line(str, asm)
        return


def remove_comment(line):
    new_line = line.split("//")
    return new_line[0]


def parse_line(line, asm_file, count, return_counter, file_name):
    # this method gets a line and sends it to be handled either as an
    # arithmetic/logic command or as a memory access command.

    line = remove_comment(line)
    split_line = line.split()
    if len(split_line) > 0:
        #first_char = split_line[0][0]
        #second_char = split_line[0][1]
        #if first_char == '/' and second_char == '/':
        #   return count, return_counter
        write_line("\n", asm_file)
        command = split_line[0]
        if len(split_line) > 1:
            if command == "push" or command == "pop":
                segment = split_line[1]
                i = split_line[2]
                handle_memory_command(command, segment, i, asm_file, file_name)
                return count, return_counter
            elif command == "function":
                return_counter = def_function(file_name, split_line[1], split_line[2], return_counter, asm_file)
            elif command == "call":
                return_counter = call_funct(file_name, split_line[1], split_line[2], return_counter, asm_file)
            elif command == "label":
                label_dec(split_line[1], asm_file)
            elif command == "goto":
                goto_label(split_line[1], asm_file)
            elif command == "if-goto":
                if_goto_label(split_line[1], asm_file)
        elif split_line[0] == "return":
            return_counter = funct_return(file_name, return_counter, asm_file)
        else:
            count = handle_arithmetic_logic_command(command, asm_file, count)
        return count, return_counter
    return count, return_counter

def handle_file(full_path, asm_file):
    vm_file = open(full_path, "r")
    file_name = os.path.basename(vm_file.name).split(".")[0]
    lines = vm_file.readlines()
    counter = 0
    return_counter = 0
    for line in lines:
        counter, return_counter = parse_line(line, asm_file, counter, return_counter, file_name)
    vm_file.close()


path = sys.argv[1]
full_path = os.path.abspath(path)
opening_line = "\n@256 \nD = A \n@SP \nM = D"
if os.path.isfile(full_path):
    asm_file = open(full_path.split(".")[0] + ".asm", "w")
    write_line(opening_line, asm_file)
    handle_file(full_path, asm_file)
elif os.path.isdir(full_path):
    directory_name = os.path.basename(full_path)
    new_path = os.path.join(full_path, directory_name)
    asm_file = open(new_path + ".asm", "w")
    files = os.listdir(full_path)
    write_line(opening_line, asm_file)
    for file in files:
        if os.path.basename(file) == "Sys.vm":
            call_funct("Sys", "Sys.init", "0", 0, asm_file)
            break
    for file in files:
        if file.split(".")[1] == "vm":
            handle_file(os.path.join(full_path, file), asm_file)
asm_file.close()
