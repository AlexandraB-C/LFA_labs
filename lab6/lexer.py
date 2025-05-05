import re
from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()
    OPERATOR = auto()
    FUNCTION = auto()
    LPAREN = auto()
    RPAREN = auto()
    ASSIGNMENT = auto()
    EOF = auto()

class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position
    
    def __str__(self):
        return f"Token({self.type}, '{self.value}', pos={self.position})"
    
    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        
        self.token_specs = [
            (TokenType.NUMBER, r'\d+(\.\d*)?|\.\d+'),
            (TokenType.FUNCTION, r'sin|cos'),
            (TokenType.IDENTIFIER, r'[a-zA-Z_]\w*'),
            (TokenType.OPERATOR, r'[+\-*/^]'),
            (TokenType.LPAREN, r'\('),
            (TokenType.RPAREN, r'\)'),
            (TokenType.ASSIGNMENT, r'='),
        ]
        
        self.token_regex = re.compile(
            '|'.join(f'(?P<{tok.name}>{pattern})' for tok, pattern in self.token_specs)
        )

    def error(self):
        raise Exception(f"Invalid character '{self.current_char}' at position {self.pos}")

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.pos += 1
            self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def tokenize(self):
        tokens = []
        while self.pos < len(self.text):
            self.skip_whitespace()
            if not self.current_char:
                break
            match = self.token_regex.match(self.text, self.pos)
            if not match:
                self.error()

            tok_type = None
            for typ, _ in self.token_specs:
                if match.group(typ.name):
                    tok_type = typ
                    break

            value = match.group(tok_type.name)
            tokens.append(Token(tok_type, value, self.pos))
            self.pos = match.end()
            self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

        tokens.append(Token(TokenType.EOF, None, self.pos))
        return tokens