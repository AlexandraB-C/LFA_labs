from lexer import Lexer, TokenType

def main():
    test_expressions = [
        "x = 10 + 5",
        "result = sin(0.5) + cos(3.14)",
        "a = 2 * (b + c)",
        "3.14159 + 42",
        
        "3..14 + 2",
        "var_name_ = 123",
        "sin(cos(x))",
        "a++b",
        "",
        "   ",
        "123abc",
        ".5 + 2",
    ]
    
    for expr in test_expressions:
        print(f"\nInput: '{expr}'")
        lexer = Lexer(expr)
        tokens = lexer.tokenize()
        
        if tokens:
            for token in tokens:
                if token.type != TokenType.EOF:
                    print(f"  {token}")
        else:
            print("  Tokenization failed")

if __name__ == "__main__":
    main()