

class CompilationEngine:

    KEYWORD = "keyword"
    SYMBOL = "symbol"
    IDENTIFIER = "identifier"
    INT_CONST = "int_const"
    STRING_CONST = "string_const"

    keyword = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int',
               'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if',
               'else', 'while', 'return']

    symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

    def __init__(self, token_obj, file):
        self.xml_file = open(file, 'w')
        self.token_obj = token_obj
        self.indent = 0

    def write_token(self, token, token_type):
        # think about identation
        self.xml_file.write("  "*self.indent + '<' + token_type + '> ')
        self.xml_file.write(token)
        self.xml_file.write(' </' + token_type + '>\n')

    # there is API with explanation in slide 114
    def compileClass(self):
        self.xml_file.write("<class>" + "\n")
        self.indent += 1
        self.write_token(self.token_obj.returnCurrentToken(), self.KEYWORD)  # write class
        self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.IDENTIFIER)  # write class name
        self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '{'
        self.token_obj.advance()
        while self.token_obj.returnCurrentToken() in {"field", "static"}:
            self.compileClassVarDec()
        self.compileSubroutineDec()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '}'
        self.token_obj.advance()
        self.xml_file.write("</class>" + "\n")

    def compileClassVarDec(self):
        self.xml_file.write("  "*self.indent + "<classVarDec>" + "\n")
        self.indent += 1
        # if...
        self.write_token(self.token_obj.returnCurrentToken(), self.KEYWORD)  # write static or field
        self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write type
        self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.IDENTIFIER)  # write variable name
        self.token_obj.advance()
        while self.token_obj.returnCurrentToken() != ';':  # for declaration of multiple variables in one line
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())# write variable name or ,
            self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write ;
        self.token_obj.advance()
        self.indent -= 1
        self.xml_file.write("  "*self.indent + "</classVarDec>" + "\n")

    def compileSubroutineDec(self):
        token = self.token_obj.returnCurrentToken()
        while token == "constructor" or token == "function" or token == "method":
            self.xml_file.write("  "*self.indent + "<subroutineDec>" + "\n")
            self.indent += 1
            self.write_token(self.token_obj.returnCurrentToken(), self.KEYWORD)  # write constructor/function/method
            self.token_obj.advance()
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write return type
            self.token_obj.advance()
            self.write_token(self.token_obj.returnCurrentToken(), self.IDENTIFIER)  # write function name
            self.token_obj.advance()
            self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '('
            self.token_obj.advance()
            self.compileParameterList()
            self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write ')'
            self.token_obj.advance()
            self.compileSubroutineBody()
            self.indent -= 1
            self.xml_file.write("  "*self.indent + "</subroutineDec>" + "\n")
            token = self.token_obj.returnCurrentToken()

    def compileParameterList(self):
        self.xml_file.write("  "*self.indent + "<parameterList>" + "\n")
        self.indent += 1
        if self.token_obj.returnCurrentToken() != ")":
            self.write_token(self.token_obj.returnCurrentToken(), self.KEYWORD)  # write type
            self.token_obj.advance()
            self.write_token(self.token_obj.returnCurrentToken(), self.IDENTIFIER)  # write variable name
            self.token_obj.advance()
        while self.token_obj.returnCurrentToken() != ")":
            self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write ','
            self.token_obj.advance()
            self.write_token(self.token_obj.returnCurrentToken(), self.KEYWORD)  # write type
            self.token_obj.advance()
            self.write_token(self.token_obj.returnCurrentToken(), self.IDENTIFIER)  # write variable name
            self.token_obj.advance()
        self.indent -= 1
        self.xml_file.write("  "*self.indent + "</parameterList>" + "\n")

    def compileSubroutineBody(self):
        self.xml_file.write("  "*self.indent + "<subroutineBody>" + "\n")
        self.indent += 1
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '{'
        self.token_obj.advance()
        self.compileVarDec()
        self.compileStatements()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '}'
        self.token_obj.advance()
        self.indent -= 1
        self.xml_file.write("  "*self.indent + "</subroutineBody>" + "\n")

    def compileVarDec(self):
        if self.token_obj.returnCurrentToken() == "var":
            self.xml_file.write("  "*self.indent + "<varDec>" + "\n")
            self.indent += 1
            self.write_token(self.token_obj.returnCurrentToken(), self.KEYWORD)  # write var
            self.token_obj.advance()
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write type
            self.token_obj.advance()
            self.write_token(self.token_obj.returnCurrentToken(), self.IDENTIFIER)  # write variable name
            self.token_obj.advance()
            while self.token_obj.returnCurrentToken() != ';':  # for declaration of multiple variables in one line
                self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write ,
                self.token_obj.advance()
                self.write_token(self.token_obj.returnCurrentToken(), self.IDENTIFIER)  # write variable name
                self.token_obj.advance()
            self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write ';'
            self.token_obj.advance()
            self.indent -= 1
            self.xml_file.write("  "*self.indent + "</varDec>" + "\n")
            self.compileVarDec()

    def compileStatements(self):
        self.xml_file.write("  " * self.indent + "<statements>" + "\n")
        self.indent += 1
        token = self.token_obj.returnCurrentToken()
        while token in {'let', 'if', 'while', 'do', 'return'}:
            if token == 'let':
                self.compileLet()

            if token == 'if':
                self.compileIf()

            if token == 'while':
                self.compileWhile()

            if token == 'do':
                self.compileDo()

            if token == 'return':
                self.compileRerurn()

            token = self.token_obj.returnCurrentToken()
        self.indent -= 1
        self.xml_file.write("  " * self.indent + "</statements>" + "\n")

    def compileLet(self):
        self.xml_file.write("  "*self.indent + "<letStatement>" + "\n")
        self.indent += 1
        self.write_token(self.token_obj.returnCurrentToken(), self.KEYWORD)  # write let
        self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.IDENTIFIER)  # write variable name
        self.token_obj.advance()
        if self.token_obj.returnCurrentToken() == '[':
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write [
            self.token_obj.advance()
            self.compileExpression()  # ?
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())
            self.token_obj.advance()

        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '='
        self.token_obj.advance()
        self.compileExpression()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write ;
        self.token_obj.advance()
        self.indent -= 1
        self.xml_file.write("  "*self.indent + "</letStatement>" + "\n")

    def compileIf(self):
        self.xml_file.write("  "*self.indent + "<ifStatement>" + "\n")
        self.indent += 1
        self.write_token(self.token_obj.returnCurrentToken(), self.KEYWORD)  # write if
        self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '('
        self.token_obj.advance()
        self.compileExpression()
        #self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write ')'
        self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '{'
        self.token_obj.advance()
        self.compileStatements()
        #self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '}'
        self.token_obj.advance()

        # handle 'else' :
        if self.token_obj.returnCurrentToken() == 'else':
            self.write_token(self.token_obj.returnCurrentToken(), self.KEYWORD)  # write else
            self.token_obj.advance()
            self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '{'
            self.token_obj.advance()
            self.compileStatements()
            #self.token_obj.advance()
            self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '}'
            self.token_obj.advance()
        self.indent -= 1
        self.xml_file.write("  "*self.indent + "</ifStatement>" + "\n")

    def compileWhile(self):
        self.xml_file.write("  "*self.indent + "<whileStatement>" + "\n")
        self.indent += 1
        self.write_token(self.token_obj.returnCurrentToken(), self.KEYWORD)  # write while
        self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '('
        self.token_obj.advance()
        self.compileExpression()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write ')'
        self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '{'
        self.token_obj.advance()
        self.compileStatements()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '}'
        self.token_obj.advance()
        self.indent -= 1
        self.xml_file.write("  "*self.indent + "</whileStatement>" + "\n")

    def compileDo(self):
        self.xml_file.write("  "*self.indent + "<doStatement>" + "\n")
        self.indent += 1
        self.write_token(self.token_obj.returnCurrentToken(), self.KEYWORD)  # write do
        self.token_obj.advance()
        while self.token_obj.returnCurrentToken() != "(":
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write subroutine name
            self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write '('
        self.token_obj.advance()
        self.compileExpressionList()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write ')'
        self.token_obj.advance()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write ;
        self.token_obj.advance()
        self.indent -= 1
        self.xml_file.write("  "*self.indent + "</doStatement>" + "\n")

    def compileRerurn(self):
        self.xml_file.write("  "*self.indent + "<returnStatement>" + "\n")
        self.indent += 1
        self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write return
        self.token_obj.advance()
        if self.token_obj.returnCurrentToken() != ";":
            self.compileExpression()
        self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)  # write ;
        self.token_obj.advance()
        self.indent -= 1
        self.xml_file.write("  "*self.indent + "</returnStatement>" + "\n")

    def compileExpression(self):
        self.xml_file.write("  " * self.indent + "<expression>" + "\n")
        self.indent += 1
        self.compileTerm()
        if self.token_obj.returnCurrentToken() not in {";", ")", ",", "]"}:
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())
            self.token_obj.advance()
            self.compileTerm()
        self.indent -= 1
        self.xml_file.write("  " * self.indent + "</expression>" + "\n")

    def compileTerm(self):
        self.xml_file.write("  " * self.indent + "<term>" + "\n")
        self.indent += 1
        self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())
        if self.token_obj.returnCurrentToken() == "(":  # if it's an expression
            self.token_obj.advance()
            self.compileExpression()
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write )
        if self.token_obj.returnCurrentToken() in {"-", "~"}:  # if it's a unaryOp
            self.token_obj.advance()
            self.compileTerm()
            self.indent -= 1
            self.xml_file.write("  " * self.indent + "</term>" + "\n")
            return
        self.token_obj.advance()
        if self.token_obj.returnCurrentToken() == ".":  # if it's a subroutine call
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType()) # write .
            self.token_obj.advance()
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write func name
            self.token_obj.advance()
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write (
            self.token_obj.advance()
            self.compileExpressionList()
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write )
            self.token_obj.advance()
        if self.token_obj.returnCurrentToken() == "[":  # if it's a varname[expression]
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write [
            self.token_obj.advance()
            self.compileExpression()
            self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write ]
            self.token_obj.advance()
        self.indent -= 1
        self.xml_file.write("  " * self.indent + "</term>" + "\n")

    def compileExpressionList(self):
        self.xml_file.write("  " * self.indent + "<expressionList>" + "\n")
        self.indent += 1
        while self.token_obj.returnCurrentToken() != ")":
            self.compileExpression()
            if self.token_obj.returnCurrentToken() == ",":
                self.write_token(self.token_obj.returnCurrentToken(), self.SYMBOL)
                self.token_obj.advance()
        self.indent -= 1
        self.xml_file.write("  " * self.indent + "</expressionList>" + "\n")