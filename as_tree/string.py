class String():
    def __init__(self, value):
        self.value = value

    def invariant(self):
        return isinstance(self.value, str)
    
    def interpret(self, env={}):
        return self.value
    
    def to_string(self, tabs=0):
        string = ""
        for i in range(tabs):
            string += self.tab
        string += "|-> " + self.value
        return string
    
    def __str__(self):
        return self.value