import VMWriter
import SymbolTable


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

    op_dict = {"+": "add", "-": "sub", "=": "eq", "&gt;": "gt", "&lt;": "lt", "&amp;": "and", "|": "or", "~": "not"}

    def __init__(self, token_obj, file):
    #    self.xml_file = open(file, 'w')
        self.token_obj = token_obj
        self.vm_file = open(file, 'w')
        self.vmWriter = VMWriter.VMWriter(self.vm_file)
        self.symbolTable = SymbolTable.SymbolTable()
        self.counter = 0
        self.class_name = None

    # def write_token(self, token, token_type):
    #     # think about identation
    #     self.xml_file.write("  "*self.indent + '<' + token_type + '> ')
    #     self.xml_file.write(token)
    #     self.xml_file.write(' </' + token_type + '>\n')

    # there is API with explanation in slide 114
    def compileClass(self):
        self.token_obj.advance()        # skip 'class'
        self.class_name = self.token_obj.returnCurrentToken()
        self.token_obj.advance()        # skip class name
        self.token_obj.advance()        # skip '{'
        while self.token_obj.returnCurrentToken() in {"field", "static"}:
            self.compileClassVarDec()
        self.compileSubroutineDec()
        self.token_obj.advance()        # skip '}'

    def compileClassVarDec(self):
        kind = self.token_obj.returnCurrentToken()
        self.token_obj.advance()
        type = self.token_obj.returnCurrentToken()
        self.token_obj.advance()
        name = self.token_obj.returnCurrentToken()
        self.token_obj.advance()
        self.symbolTable.define(name, type, kind.upper())
        while self.token_obj.returnCurrentToken() != ';':  # for declaration of multiple variables in one line
            self.token_obj.advance()                        # skip ,
            name = self.token_obj.returnCurrentToken()
            self.token_obj.advance()
            self.symbolTable.define(name, type, kind.upper())
        self.token_obj.advance()                          # skip ;

    def compileSubroutineDec(self):
        token = self.token_obj.returnCurrentToken()
        while token == "constructor" or token == "function" or token == "method":
            type = self.token_obj.returnCurrentToken()  # saves constructor/function/method
            self.token_obj.advance()
            #self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write return type
            self.token_obj.advance()        # skip return type
            name = self.token_obj.returnCurrentToken()  # save function name
            function_name = self.class_name + "." + name
            self.token_obj.advance()

            self.symbolTable.startSubroutine()
            self.token_obj.advance()        # skip '('
            if type == "method":
                self.symbolTable.define("this", self.class_name, "ARG")
            self.compileParameterList()
            self.token_obj.advance()        # skip ')'

            self.token_obj.advance()  # skip '{'
            vars_count = self.compileVarDec()
            self.vmWriter.writeFunction(function_name, str(vars_count))       #TODO: nvars ???

            if type == "constructor":
                self.vmWriter.writePush("constant", self.symbolTable.varCount("FIELD"))
                self.vmWriter.writeCall("Memory.alloc", "1")
                self.vmWriter.writePop("pointer", "0")
            if type == "method":
                self.vmWriter.writePush("argument", "0")
                self.vmWriter.writePop("pointer", "0")
            self.compileSubroutineBody()
            token = self.token_obj.returnCurrentToken()

    def compileParameterList(self):
        if self.token_obj.returnCurrentToken() != ")":
            type = self.token_obj.returnCurrentToken()
            self.token_obj.advance()
            name = self.token_obj.returnCurrentToken()
            self.token_obj.advance()
            self.symbolTable.define(name, type, "ARG")
        while self.token_obj.returnCurrentToken() != ")":
            self.token_obj.advance()                   # skip ','
            type = self.token_obj.returnCurrentToken()
            self.token_obj.advance()
            name = self.token_obj.returnCurrentToken()
            self.token_obj.advance()
            self.symbolTable.define(name, type, "ARG")

    def compileSubroutineBody(self):
        self.compileStatements()
        self.token_obj.advance()        # skip '}'

    def compileVarDec(self):
        vars_count = 0
        if self.token_obj.returnCurrentToken() == "var":
            kind = self.token_obj.returnCurrentToken()
            self.token_obj.advance()
            type = self.token_obj.returnCurrentToken()
            self.token_obj.advance()
            name = self.token_obj.returnCurrentToken()
            self.token_obj.advance()
            self.symbolTable.define(name, type, kind.upper())
            vars_count += 1
            while self.token_obj.returnCurrentToken() != ';':  # for declaration of multiple variables in one line
                self.token_obj.advance()            # skip ,
                name = self.token_obj.returnCurrentToken()
                self.token_obj.advance()
                self.symbolTable.define(name, type, kind.upper())
                vars_count += 1
            self.token_obj.advance()        # skip ;
            vars_count += self.compileVarDec()
        return vars_count

    def compileStatements(self):
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



    def compileLet(self):
        self.token_obj.advance()        # skip let

        isArrayAccess, varName = self.compileTerm()
        if not isArrayAccess:
            self.vmWriter.writePop("temp", "0")

        self.token_obj.advance()        # skip '='

        self.compileExpression()        # push right side
        self.vmWriter.writePop("temp", "1")

        if isArrayAccess:
            self.vmWriter.writePop("pointer", "1")
            self.vmWriter.writePush("temp", "1")
            self.vmWriter.writePop("that", "0")

        else:
            self.vmWriter.writePush("temp", "1")
            kind = self.symbolTable.kindOf(varName)
            if kind == "FIELD":
                kind = "this"
            self.vmWriter.writePop(kind, self.symbolTable.indexOf(varName))

        self.token_obj.advance()        # skip ;

    def compileIf(self):

        self.token_obj.advance()        # skip 'if'
        self.token_obj.advance()        # skip (
        self.compileExpression()        # push the expression
        self.token_obj.advance()        # skip )

        self.vmWriter.writeArithmetic("not")
        label_name = self.class_name + "." + str(self.counter)
        self.counter += 1

        self.vmWriter.writeIf(label_name)
        self.token_obj.advance()        # skip {
        self.compileStatements()
        self.token_obj.advance()        # skip }


        # handle 'else' :
        if self.token_obj.returnCurrentToken() == 'else':

            after_label = self.class_name + "." + str(self.counter)
            self.counter += 1
            self.vmWriter.writeGoto(after_label)

            self.vmWriter.writeLabel(label_name)
            self.token_obj.advance()        # skip 'else'
            self.token_obj.advance()        # skip {
            self.compileStatements()
            self.token_obj.advance()        # skip }
            self.vmWriter.writeLabel(after_label)
            return

        self.vmWriter.writeLabel(label_name)
    
    def compileWhile(self):
        while_label = self.class_name + "." + str(self.counter)
        self.counter += 1
        after_label = self.class_name + "." + str(self.counter)
        self.counter += 1

        self.vmWriter.writeLabel(while_label)

        self.token_obj.advance()        # skip 'while'
        self.token_obj.advance()        # skip '('
        self.compileExpression()
        self.vmWriter.writeArithmetic("not")
        self.token_obj.advance()        # skip ')'

        self.vmWriter.writeIf(after_label)

        self.token_obj.advance()        # skip '{'
        self.compileStatements()
        self.token_obj.advance()        # skip '}'

        self.vmWriter.writeGoto(while_label)
        self.vmWriter.writeLabel(after_label)

    def compileDo(self):
        self.token_obj.advance()        # skip 'do'
        subroutine_name = ""
        first_arg = None
        first_arg_kind = None
        first_arg_index = None
        arg_counter = 0

        while self.token_obj.returnCurrentToken() != "(":
            if self.symbolTable.isInTable(self.token_obj.returnCurrentToken()):
                subroutine_name += self.symbolTable.typeOf(self.token_obj.returnCurrentToken()) # save subroutine name
                first_arg = self.token_obj.returnCurrentToken()
                first_arg_kind = self.symbolTable.kindOf(first_arg)
                if first_arg_kind == "FIELD":
                    first_arg_kind = "this"
                first_arg_index = self.symbolTable.indexOf(first_arg)
                arg_counter += 1

            else:
                subroutine_name += self.token_obj.returnCurrentToken()  # save subroutine name
            self.token_obj.advance()
        if "." not in subroutine_name:
            subroutine_name = self.class_name + "." + subroutine_name
            self.vmWriter.writePush("pointer", "0")
            arg_counter += 1
        self.token_obj.advance()        # skip '('
        if first_arg:
            self.vmWriter.writePush(first_arg_kind, first_arg_index)
        arg_counter += self.compileExpressionList()
        self.vmWriter.writeCall(subroutine_name, str(arg_counter))
        self.token_obj.advance()        # skip ')'
        self.token_obj.advance()        # skip ';'
        self.vmWriter.writePop("temp", "0")

    def compileRerurn(self):
        self.token_obj.advance()        # skip 'return'
        if self.token_obj.returnCurrentToken() != ";":
            self.compileExpression()
        else:
            self.vmWriter.writePush("constant", 0)
        self.vmWriter.writeRerutn()
        self.token_obj.advance()        # skip ';'

    def compileExpression(self):
        isArrayAccess, doesntMatter = self.compileTerm()
        if isArrayAccess:
            self.vmWriter.writePop("pointer", "1")
            self.vmWriter.writePush("that", "0")
        if self.token_obj.returnCurrentToken() not in {";", ")", ",", "]"}:
            op = self.token_obj.returnCurrentToken()        # save op
            self.token_obj.advance()
            isArrayAccess, doesntMatter = self.compileTerm()
            if isArrayAccess:
                self.vmWriter.writePop("pointer", "1")
                self.vmWriter.writePush("that", "0")
            if op == "*":
                self.vmWriter.writeCall("Math.multiply", "2")
            if op == "/":
                self.vmWriter.writeCall("Math.divide", "2")
            if op in CompilationEngine.op_dict:
                self.vmWriter.writeArithmetic(CompilationEngine.op_dict[op])

    def compileTerm(self):
        if self.token_obj.tokenType() == "integerConstant":
            self.vmWriter.writePush("constant", self.token_obj.returnCurrentToken())
            self.token_obj.advance()
            return False, ""

        if self.token_obj.tokenType() == "stringConstant":      # TODO:strings
            self.vmWriter.writePush("constant", str(len(self.token_obj.returnCurrentToken())))
            self.vmWriter.writeCall("String.new", "1")
            for letter in self.token_obj.returnCurrentToken():
                self.vmWriter.writePush("constant", str(ord(letter)))
                self.vmWriter.writeCall("String.appendChar", "2")
            self.token_obj.advance()
            return False, ""

        if self.token_obj.tokenType() == "keyword":
            if self.token_obj.returnCurrentToken() == "true":
                self.vmWriter.writePush("constant", "1")
                self.vmWriter.writeArithmetic("neg")
                self.token_obj.advance()
                return False, ""
            if self.token_obj.returnCurrentToken() == "false" or self.token_obj.returnCurrentToken() == "null":
                self.vmWriter.writePush("constant", "0")
                self.token_obj.advance()
                return False, ""
            if self.token_obj.returnCurrentToken() == "this":
                self.vmWriter.writePush("pointer", "0")
                self.token_obj.advance()
                return False, ""

        varName = ""
        if self.symbolTable.isInTable(self.token_obj.returnCurrentToken()):
            if self.symbolTable.isInTable(self.token_obj.returnCurrentToken()):
                varName = self.token_obj.returnCurrentToken()
                kind = self.symbolTable.kindOf(self.token_obj.returnCurrentToken())
                if kind == "FIELD":
                    kind = "this"
                self.vmWriter.writePush(kind, self.symbolTable.indexOf(self.token_obj.returnCurrentToken()))
            self.token_obj.advance()

            if self.token_obj.returnCurrentToken() == "[":       # if it's a varname[expression]
                #self.vmWriter.writePush(self.symbolTable.kindOf(hold_on), self.symbolTable.indexOf(hold_on))
                self.token_obj.advance()        # skip '['
                self.compileExpression()
                self.token_obj.advance()        # skip ']'
                self.vmWriter.writeArithmetic("add")
                return True, ""
            if self.token_obj.returnCurrentToken() == ".":  # if it's a subroutine call
                self.token_obj.advance()  # skip '.'
                funct_name = self.token_obj.returnCurrentToken()
                self.token_obj.advance()
                self.token_obj.advance()  # skip '('
                arg_counter = self.compileExpressionList()
                self.token_obj.advance()  # skip ')'
                self.vmWriter.writeCall(self.symbolTable.typeOf(varName) + "." + funct_name, str(arg_counter + 1))
                return False, ""
            else:
                return False, varName

        if self.token_obj.returnCurrentToken() == "(":  # if it's an expression
            self.token_obj.advance()
            self.compileExpression()
            #self.write_token(self.token_obj.returnCurrentToken(), self.token_obj.tokenType())  # write )

        if self.token_obj.returnCurrentToken() in {"-", "~"}:  # if it's a unaryOp
            unaryOp = self.token_obj.returnCurrentToken()
            self.token_obj.advance()
            self.compileTerm()
            if unaryOp == "-":
                self.vmWriter.writeArithmetic("neg")
            if unaryOp == "~":
                self.vmWriter.writeArithmetic("not")
            return False, ""

        hold_on = self.token_obj.returnCurrentToken()

        self.token_obj.advance()

        if self.token_obj.returnCurrentToken() == ".":          # if it's a subroutine call
            self.token_obj.advance()        # skip '.'
            funct_name = self.token_obj.returnCurrentToken()
            self.token_obj.advance()
            self.token_obj.advance()         # skip '('
            arg_counter = self.compileExpressionList()
            self.token_obj.advance()        # skip ')'
            self.vmWriter.writeCall(hold_on + "." + funct_name, str(arg_counter))

        if self.token_obj.returnCurrentToken() == "(":  # if it's a function call
            self.token_obj.advance()  # skip '('
            arg_counter = self.compileExpressionList()
            self.token_obj.advance()  # skip ')'
            self.vmWriter.writeCall(self.class_name + "." + hold_on, str(arg_counter))

        return False, varName


    def compileExpressionList(self):
        arg_counter = 0
        while self.token_obj.returnCurrentToken() != ")":
            arg_counter += 1
            self.compileExpression()
            if self.token_obj.returnCurrentToken() == ",":
                self.token_obj.advance()        # skip ','
        return arg_counter
