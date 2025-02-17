# main.py
from grammar import Grammar

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
    
    grammar = Grammar(vn, vt, p, s)
    
    print("5 strings gen from the grammar:")
    generated_strings = grammar.generate_strings(5)
    for i, string in enumerate(generated_strings, 1):
        print(f"{i}. {string}")

if __name__ == "__main__":
    main()