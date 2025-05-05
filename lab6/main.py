from lexer import Lexer
from parser import Parser, print_ast

def main():
    test_exprs = [
        "x = 10 + 5",
        "result = sin(0.5) + cos(3.14)",
        "a = 2 * (b + c)",
        "3.14159 + 42",
        "sin(cos(x))",
        # invalid inputs
        "3..14 + 2",
        "var_name_ = 123",
        "a++b",
        "sin()",
        "5 = x",
        "",
        "   ",
    ]
    
    for expr in test_exprs:
        print(f"\nInput: '{expr}'")
        
        # lexical analysis
        lexer = Lexer(expr)
        tokens = lexer.tokenize()
        
        if not tokens:
            print("-----Tokenization failed------")
            continue
        
        for i, token in enumerate(tokens):
            if token.type.name != "EOF":
                print(f"  {token}")
        
        # parsing and AST constr
        parser = Parser(tokens)
        ast = parser.parse()
        
        if ast:
            print("\nAbstract Syntax Tree:")
            print_ast(ast)
        else:
            print("\n------Abstract Syntax Tree construction failed-----")


if __name__ == "__main__":
    main()