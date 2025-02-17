import random

class Grammar:
    def __init__(self, vn, vt, p, s):
        self.vn = vn
        self.vt = vt
        self.p = p
        self.s = s
        
    def generate_string(self, symbol=None, max_depth=10):

        if max_depth <= 0:  # prevent infinite recursion
            return ""
        
        if symbol is None:
            symbol = self.s
        
        if symbol in self.vt:
            return symbol
        
        # get all 
        productions = [rule[1] for rule in self.p if rule[0] == symbol]
        
        if not productions:  # no rules for this symbol
            return ""
        
        chosen = random.choice(productions)
        result = ""
        
        for s in chosen:
            result += self.generate_string(s, max_depth - 1)
            
        return result
    
    def generate_strings(self, count=5):
        """generates multiple strings from the grammar"""
        return [self.generate_string() for _ in range(count)]