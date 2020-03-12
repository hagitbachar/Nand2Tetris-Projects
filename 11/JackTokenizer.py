import string

class JackTokenizer:
    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "integerConstant"
    STRING_CONST = "stringConstant"

    keyword = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int',
               'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if',
               'else', 'while', 'return']

    symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']


    def __init__(self, input_file):
        self.file = input_file
        self.token_list = self.createTokenList()
        self.current_token = ""
        self.index = 0
        self.current_token = self.advance()


    def hasMoreTokens(self):
        if len(self.token_list) > self.index:
            return True
        else:
            return False


    def isCommentOrEmptyLine(self, line):
        if line.startswith('\n') or line.startswith('//') or line.startswith('/**') or line.startswith('*'):
            return True

    def createTokenList(self):
        token_list = []
        file = open(self.file).read()
        lines = file.split('\n')
        token = ""
        for line in lines:
            line = line.lstrip()
            if self.isCommentOrEmptyLine(line):
                continue
            counter = 0
            while counter < len(line):
                if line[counter:].startswith('//'):
                    if token != "":
                        token_list.append(token)
                    token = ""
                    counter = len(line)
                elif line[counter] == '"':
                    token += line[counter]
                    counter += 1
                    while line[counter] != '"':
                        token += line[counter]
                        counter += 1
                    token += line[counter]
                    counter += 1
                    token_list.append(token)
                    token = ""
                elif line[counter:].startswith('/*'):
                    if token != "":
                        token_list.append(token)
                    token = ""
                    counter += 2
                    while not line[counter:].startswith('*/'):
                        counter += 1
                    counter += 2
                elif line[counter] in string.whitespace or line[counter] == '\n':
                    if token != "":
                        token_list.append(token)
                    token = ""
                    counter += 1
                elif line[counter] in JackTokenizer.symbol:
                    if token != "":
                        token_list.append(token)
                        token = ""
                    token_list.append(line[counter])
                    counter += 1
                else:
                    token += line[counter]
                    counter += 1

        return token_list


    def advance(self):
        if self.hasMoreTokens():
            self.current_token = self.token_list[self.index]
            self.index += 1
        return self.current_token


    def tokenType(self):
        if self.current_token in self.keyword:
            return self.KEYWORD
        elif self.current_token in self.symbol:
            return self.SYMBOL
        elif self.current_token.isdigit():
            return self.INT_CONST
        elif self.current_token.startswith('"') and self.current_token.endswith('"'):
            return self.STRING_CONST
        else:
            return self.IDENTIFIER


    def returnCurrentToken(self):
        if self.tokenType() == self.STRING_CONST:
            return self.current_token[1:-1]
        if self.current_token == "<":
            return "&lt;"
        if self.current_token == ">":
            return "&gt;"
        if self.current_token == '"':
            return "&qout;"
        if self.current_token == "&":
            return "&amp;"
        return self.current_token
