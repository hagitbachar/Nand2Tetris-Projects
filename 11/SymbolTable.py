
class SymbolTable:

    """
        Create a new symbol table
    """
    def __init__(self):
        self.class_table = {}
        self.subroutine_table = {}

        # class indexes
        self.static_index = 0
        self.field_index = 0

        # subroutine indexes
        self.arg_index = 0
        self.var_index = 0

    """
        Start a new subroutine scope
    """
    def startSubroutine(self):
        self.subroutine_table.clear()
        self.arg_index = 0
        self.var_index = 0

    """
        Defines a new identifier of the given name, type, and kind,
        and assigns it a running index
    """
    def define(self, name, type, kind):
        if kind == "STATIC":
            self.class_table[name] = (type, kind, self.static_index)
            self.static_index += 1
        elif kind == "FIELD":
            self.class_table[name] = (type, kind, self.field_index)
            self.field_index += 1
        elif kind == "ARG":
            self.subroutine_table[name] = (type, "argument", self.arg_index)
            self.arg_index += 1
        elif kind == "VAR":
            self.subroutine_table[name] = (type, "local", self.var_index)
            self.var_index += 1

    """
        Returns the number of variables of the given kind already defined 
        in the current scope
    """
    def varCount(self, kind):
        if kind == "STATIC":
            return self.static_index
        elif kind == "FIELD":
            return self.field_index
        elif kind == "ARG":
            return self.arg_index
        elif kind == "VAR":
            return self.var_index

    """
        Returns the kind of the named identifiers in the current scope
    """
    def kindOf(self, name):
        kind_index = 1

        if name in self.class_table:
            return self.class_table[name][kind_index]
        elif name in self.subroutine_table:
            return self.subroutine_table[name][kind_index]
        else:
            return "None"

    """
        Returns the type of the named identifiers in the current scope
    """
    def typeOf(self, name):
        kind_index = 0

        if name in self.class_table:
            return self.class_table[name][kind_index]
        elif name in self.subroutine_table:
            return self.subroutine_table[name][kind_index]

    """
        Returns the index assigned to the named identifier
    """
    def indexOf(self, name):
        kind_index = 2

        if name in self.class_table:
            return self.class_table[name][kind_index]
        elif name in self.subroutine_table:
            return self.subroutine_table[name][kind_index]

    def isInTable(self, name):
        if name in self.class_table:
            return True
        if name in self.subroutine_table:
            return True
        return False