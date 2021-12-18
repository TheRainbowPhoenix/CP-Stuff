

class Module:
    """Collection of funtions"""

    def __init__(self, name=None):
        self.name = name
        self.headers = []
        self.functions = []
        self.interfaces = []

    def addFunctions(self, functions):
        self.functions.extend(functions)

    def addInterfaces(self, interfaces):
        self.interfaces.extend(interfaces)

    def mergeModule(self, module):
        self.headers.extend(module.headers)
        self.functions.extend(module.functions)
        self.interfaces.extend(module.interfaces)

    def getFunctionByName(self, name):
        for function in self.functions:
            if function.name == name:
                return function
        return None
