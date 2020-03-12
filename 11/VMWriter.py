

class VMWriter:

    """
        Create a new output .vm file and prepares it for writing
    """
    def __init__(self, output_file):
        self.output_file = output_file

    """
        Writes a vm push command
    """
    def writePush(self, segment, index):
        self.output_file.write("push " + segment.lower() + " " + str(index) + "\n")

    """
        Writes a vm pop command
    """
    def writePop(self, segment, index):
        self.output_file.write("pop " + segment.lower() + " " + str(index) + "\n")

    """
        Writes a vm arithmetic-logical command
    """
    def writeArithmetic(self, command):
        self.output_file.write(command.lower() + "\n")

    """
        Writes a vm label command
    """
    def writeLabel(self, lable):
        self.output_file.write("label " + lable + "\n")


    """
        Writes a vm goto command
    """
    def writeGoto(self, lable):
        self.output_file.write("goto " + lable + "\n")

    """
        Writes a vm if-goto command
    """
    def writeIf(self, lable):
        self.output_file.write("if-goto " + lable + "\n")

    """
        Writes a vm call command
    """
    def writeCall(self, name, nArgs):
        self.output_file.write("call " + name + " " + nArgs + "\n")

    """
        Writes a vm function command
    """
    def writeFunction(self, name, nLocals):
        self.output_file.write("function " + name + " "+ nLocals + "\n")

    """
        Writes a vm return command
    """
    def writeRerutn(self):
        self.output_file.write("return\n")

    """
        Closes the output file
    """
    def close(self):
        self.output_file.close()
