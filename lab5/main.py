import itertools

class Grammar:
    def __init__(self, vn=None, vt=None, p=None, s='S'):
        self.vn = vn if vn else set()
        self.vt = vt if vt else set()
        self.p = p if p else {}
        self.s = s
        
    def __str__(self):
        result = ""
        for left, right_sides in self.p.items():
            result += f"{left}->"
            result += "|".join(right_sides)
            result += "\n"
        return result


def eliminate_epsilon_productions(grammar):
    nullable = set()
    for left, right_sides in grammar.p.items():
        if 'ε' in right_sides:
            nullable.add(left)
            right_sides.remove('ε')
    changed = True
    while changed:
        changed = False
        for left, right_sides in grammar.p.items():
            for right in list(right_sides):
                if all(symbol in nullable for symbol in right) and left not in nullable:
                    nullable.add(left)
                    changed = True
    
    new_productions = {left: set(right_sides) for left, right_sides in grammar.p.items()}
    
    for left, right_sides in grammar.p.items():
        for right in list(right_sides):
            nullable_positions = [i for i, symbol in enumerate(right) if symbol in nullable]
            for k in range(1, len(nullable_positions) + 1):
                for positions in itertools.combinations(nullable_positions, k):
                    new_right = ''.join(symbol for i, symbol in enumerate(right) if i not in positions)
                    if new_right and new_right != right:
                        new_productions[left].add(new_right)
    
    grammar.p = new_productions
    return grammar

def eliminate_unit_productions(grammar):
    unit_pairs = set()
    
    for nt in grammar.vn:
        unit_pairs.add((nt, nt))
    changed = True
    while changed:
        changed = False
        for A, B in list(unit_pairs):
            for right in grammar.p.get(B, []):
                if len(right) == 1 and right in grammar.vn:
                    if (A, right) not in unit_pairs:
                        unit_pairs.add((A, right))
                        changed = True
    
    # rm unit prods
    new_productions = {left: set() for left in grammar.p}
    
    for A, B in unit_pairs:
        for right in grammar.p.get(B, []):
            if len(right) != 1 or right not in grammar.vn:
                new_productions[A].add(right)
    
    grammar.p = new_productions
    return grammar


def find_accessible_symbols(grammar):
    accessible = {grammar.s}
    changed = True
    
    while changed:
        changed = False
        for left in list(accessible):
            if left in grammar.p:
                for right in grammar.p[left]:
                    for symbol in right:
                        if symbol in grammar.vn and symbol not in accessible:
                            accessible.add(symbol)
                            changed = True
    
    return accessible


def eliminate_inaccessible_symbols(grammar):
    # rm unreachable
    accessible = find_accessible_symbols(grammar)
    grammar.vn = grammar.vn.intersection(accessible)
    grammar.p = {left: right_sides for left, right_sides in grammar.p.items() if left in accessible}
    
    return grammar


def find_productive_symbols(grammar):
    productive = set()
    
    # directly productive
    for left, right_sides in grammar.p.items():
        for right in right_sides:
            if all(symbol in grammar.vt for symbol in right):
                productive.add(left)
                break
    # indirectly productive
    changed = True
    while changed:
        changed = False
        for left, right_sides in grammar.p.items():
            if left not in productive:
                for right in right_sides:
                    if all(symbol in productive or symbol in grammar.vt for symbol in right):
                        productive.add(left)
                        changed = True
                        break
    
    return productive

def eliminate_non_productive_symbols(grammar):
    # rm non-productive
    productive = find_productive_symbols(grammar)
    
    grammar.vn = grammar.vn.intersection(productive)
    grammar.p = {left: right_sides for left, right_sides in grammar.p.items() if left in productive}
    
    # rm prods with non-productive syms
    for left, right_sides in list(grammar.p.items()):
        grammar.p[left] = {right for right in right_sides if all(
            symbol in productive or symbol in grammar.vt for symbol in right)}
    
    return grammar

def convert_to_cnf(grammar):
    terminal_replacements = {}
    new_productions = {left: set() for left in grammar.p}
    new_symbols = set()
    
    # replace terms in long rules
    for left, right_sides in grammar.p.items():
        for right in right_sides:
            if len(right) > 1:
                new_right = []
                for symbol in right:
                    if symbol in grammar.vt:
                        if symbol not in terminal_replacements:
                            new_symbol = f"T_{symbol}"
                            terminal_replacements[symbol] = new_symbol
                            new_symbols.add(new_symbol)
                            new_productions[new_symbol] = {symbol}
                        new_right.append(terminal_replacements[symbol])
                    else:
                        new_right.append(symbol)
                new_productions[left].add(''.join(new_right))
            else:
                new_productions[left].add(right)
    
    final_productions = {**new_productions}
    more_new_symbols = set()
    
    for left, right_sides in new_productions.items():
        final_productions[left] = set()
        for right in right_sides:
            if len(right) > 2:
                current_left = left
                for i in range(len(right) - 2):
                    new_symbol = f"X_{left}_{i}"
                    more_new_symbols.add(new_symbol)
                    final_productions[current_left].add(right[i] + new_symbol)
                    current_left = new_symbol
                    if new_symbol not in final_productions:
                        final_productions[new_symbol] = set()
                
                final_productions[current_left].add(right[-2:])
            else:
                final_productions[left].add(right)
    
    grammar.vn = grammar.vn.union(new_symbols).union(more_new_symbols)
    grammar.p = final_productions
    
    return grammar

def to_chomsky_normal_form(grammar):
    print("Base:")
    print(grammar)
    
    print("\n1) Eliminate ε productions")
    grammar = eliminate_epsilon_productions(grammar)
    print(grammar)
    
    print("\n2) Eliminate any renaming")
    grammar = eliminate_unit_productions(grammar)
    print(grammar)
    
    print("\n3) Eliminate inaccessible symbols")
    grammar = eliminate_inaccessible_symbols(grammar)
    print(grammar)
    
    print("\n4) Eliminate non productive symbols")
    grammar = eliminate_non_productive_symbols(grammar)
    print(grammar)
    
    print("\n5) CNF")
    grammar = convert_to_cnf(grammar)
    print(grammar)
    
    return grammar


def main():
    vn = {'S', 'A', 'B', 'C', 'D'}
    vt = {'a', 'b'}
    p = {
        'S': {'aB', 'bA', 'A'},
        'A': {'B', 'AS', 'bBAB', 'b'},
        'B': {'b', 'bS', 'aD', 'ε'},
        'D': {'AA'},
        'C': {'Ba'}
    }
    
    grammar = Grammar(vn, vt, p, 'S')
    cnf_grammar = to_chomsky_normal_form(grammar)


if __name__ == "__main__":
    main()