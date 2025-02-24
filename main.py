import random

class Grammar:
    def __init__(self, vn, vt, p, s):
        self.vn = vn
        self.vt = vt
        self.p = p
        self.s = s
        
    def gen_str(self, max_iter=50):
        curr = self.s
        i = 0
        
        while i < max_iter:
            # check no more nonterminals
            if all(sym not in self.vn for sym in curr):
                return curr
                
            possible_positions = []
            for idx, sym in enumerate(curr):
                if sym in self.vn:
                    possible_positions.append((idx, sym))
            
            if not possible_positions:
                break
                
            pos, sym = random.choice(possible_positions)
            possible_rules = [rule[1] for rule in self.p if rule[0] == sym]
            if not possible_rules:
                break
                
            new_str = random.choice(possible_rules)
            curr = curr[:pos] + new_str + curr[pos + 1:]
            i += 1
        
        return curr if all(sym not in self.vn for sym in curr) else None

    def gen_mult_strs(self, cnt=5):
        strs = set()
        tries = 0
        max_tries = cnt * 20
        
        while len(strs) < cnt and tries < max_tries:
            if res := self.gen_str():
                if all(c in self.vt for c in res):
                    strs.add(res)
            tries += 1
            
        return list(strs)

    def to_fa(self):
        # convert
        states = self.vn | {'F'}
        alpha = self.vt
        trans = {}
        init = self.s
        final = {'F'}

        for state in states:
            trans[state] = {}

        # gotta make them transition fam
        for state in self.vn:
            for rule in self.p:
                if rule[0] == state:
                    if rule[1] == 'e':
                        # empty string prod
                        final.add(state)
                    elif len(rule[1]) == 1 and rule[1] in self.vt:
                        # terminal prod
                        if rule[1] not in trans[state]:
                            trans[state][rule[1]] = set()
                        trans[state][rule[1]].add('F')
                    elif len(rule[1]) >= 2:
                        # handle longer prod
                        first_char = rule[1][0]
                        if first_char in self.vt:
                            next_state = rule[1][1] if len(rule[1]) > 1 else 'F'
                            if first_char not in trans[state]:
                                trans[state][first_char] = set()
                            trans[state][first_char].add(next_state)

        return FA(states, alpha, trans, init, final)

class FA:
    def __init__(self, states, alpha, trans, init, final):
        self.states = states
        self.alpha = alpha
        self.trans = trans
        self.init = init
        self.final = final

    def check_str(self, inp):
        # check if input valid
        if not inp and self.init in self.final:
            return True
            
        curr_states = {self.init}
        
        for c in inp:
            if c not in self.alpha:
                return False
                
            next_states = set()
            for state in curr_states:
                if state in self.trans and c in self.trans[state]:
                    next_states.update(self.trans[state][c])
            
            if not next_states:
                return False
                
            curr_states = next_states

        return any(state in self.final for state in curr_states)

def main():
    vn = {'S', 'L', 'D'}
    vt = {'a', 'b', 'c', 'd', 'e', 'f', 'j'}
    p = [
        ('S', 'aS'),
        ('S', 'bS'),
        ('S', 'cD'),
        ('S', 'dL'),
        ('S', 'e'),
        ('L', 'eL'),
        ('L', 'fL'),
        ('L', 'jD'),
        ('L', 'e'),
        ('D', 'eD'),
        ('D', 'd')
    ]
    s = 'S'

    g = Grammar(vn, vt, p, s)

    # generate
    strings = g.gen_mult_strs(5)
    for i, str in enumerate(strings, 1):
        print(f"{i}. {str}")

    # this turns FA
    fa = g.to_fa()

    # test a set set
    for s in strings:
        works = fa.check_str(s)
        print(f"'{s}' works? {works}")

    """print("\njust in case")
    test = ["e", "ae", "be", "cd", "dfd", "aaaae", "bbbe", "dejd", "invalid"]
    for t in test:
        works = fa.check_str(t)
        print(f"'{t}' works? {works}")"""

if __name__ == "__main__":
    main()