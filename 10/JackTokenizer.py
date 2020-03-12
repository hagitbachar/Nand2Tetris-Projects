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
        if line.startswith('\n') or line.startswith('//') or line.startswith('/*') or line.startswith('*'):
            return True


    def createTokenList(self):
        token_list = []
        file = open(self.file).read()
        lines = file.split('\n')
        is_string = False
        for line in lines:
            line = line.lstrip()
            if self.isCommentOrEmptyLine(line):
                continue
            line = line.split("//")[0]
            token = ""
            for c in line:
                if c == '"':
                    is_string = not is_string
                if not is_string:
                    if c in string.whitespace:
                        if token != "":
                            token_list.append(token)
                        token = ""
                        continue
                if c in JackTokenizer.symbol:
                    if token != "":
                        token_list.append(token)
                    token_list.append(c)
                    token = ""
                    continue
                token += c
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
