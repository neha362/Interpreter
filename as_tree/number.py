from as_tree.factor import *

# class Number extends the Factor node and implements the interpret method according to the BNF rule (number := INTEGER* | INTEGER* PERIOD INTEGER)
class Number(Factor):
    def __init__(self, values, neg=False):
        self.values = values
        self.neg = neg
    
    # every emlement in the list, either ht e
    def invariant(self):
        for i in self.values:
            if not (i.name == INTEGER or i.name == PERIOD):
                return False
        return len([x for x in self.values if x.name == PERIOD]) <= 1

    # returns the decimal value of the number
    def interpret(self, env={}):
        if not self.invariant():
            raise Exception("illegal number node")
        value = ("".join([str(i.symbol) for i in self.values]))
        value = int(value) if str.isdecimal(value) else float(value)
        return value * (-1 if self.neg else 1)

    # prints out the number, as represented by the array of symbols
    def to_string(self, tabs=0):
        string = ""
        for _ in range(tabs):
            string += self.tab
        return string + "|-> " + type(self).__name__ + ", " + ("-" if self.neg else "") + str([i.symbol for i in self.values])

    # prints out the number, as represented by the array of symbols
    def __str__(self):
        return ("-" if self.neg else "") + "".join([str(i.symbol) for i in self.values])
    