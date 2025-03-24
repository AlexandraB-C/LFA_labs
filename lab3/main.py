from lexer import Lexer, TokenType

def main():
    # test cases including edge cases
    test_expressions = [
        # basic expressions
        "x = 10 + 5",
        "result = sin(0.5) + cos(3.14)",
        "a = 2 * (b + c)",
        "3.14159 + 42",
        
        # edge cases
        "3..14 + 2",  # invalid float
        "var_name_ = 123",  # identifier with underscore
        "sin(cos(x))",  # nested functions
        "a++b",  # consecutive operators
        "",  # empty string
        "   ",  # whitespace only
        "123abc",  # invalid identifier starting with number
        ".5 + 2",  # decimal starting with dot
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