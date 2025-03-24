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
        self.current_char = self.text[self.pos] if len(self.text) > 0 else None
        
        # supported functions
        self.functions = ['sin', 'cos']
        
        # supported operators
        self.operators = ['+', '-', '*', '/', '^']
    
    def error(self):
        # simple error msg
        raise Exception(f"invalid char '{self.current_char}' at position {self.pos}")
    
    def advance(self):
        # move position pointer and update current_char
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
    
    def skip_whitespace(self):
        # skip spaces and tabs etc
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def number(self):
        # handle both int and float nums
        result = ''
        start_pos = self.pos
        decimal_point = False
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if decimal_point:  # already saw one decimal point
                    break
                decimal_point = True
            result += self.current_char
            self.advance()
        
        # handle edge cases
        if result == '.':
            raise Exception(f"invalid number format at position {start_pos}")
        
        # convert to appropriate type
        if '.' in result:
            try:
                return Token(TokenType.NUMBER, float(result), start_pos)
            except ValueError:
                raise Exception(f"invalid float format at position {start_pos}")
        else:
            try:
                return Token(TokenType.NUMBER, int(result), start_pos)
            except ValueError:
                raise Exception(f"invalid integer format at position {start_pos}")
    
    def identifier(self):
        # handle var names and keywords
        result = ''
        start_pos = self.pos
        
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        # empty identifier check
        if not result:
            raise Exception(f"empty identifier at position {start_pos}")
        
        # check if its a function
        if result in self.functions:
            return Token(TokenType.FUNCTION, result, start_pos)
        
        return Token(TokenType.IDENTIFIER, result, start_pos)
    
    def get_next_token(self):
        # main tokenizing method
        while self.current_char is not None:
            
            # handle whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # handle numbers
            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()
            
            # handle identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            
            # handle operators
            if self.current_char in self.operators:
                token = Token(TokenType.OPERATOR, self.current_char, self.pos)
                self.advance()
                return token
            
            # handle parentheses
            if self.current_char == '(':
                token = Token(TokenType.LPAREN, self.current_char, self.pos)
                self.advance()
                return token
            
            if self.current_char == ')':
                token = Token(TokenType.RPAREN, self.current_char, self.pos)
                self.advance()
                return token
            
            # handle assignment
            if self.current_char == '=':
                token = Token(TokenType.ASSIGNMENT, self.current_char, self.pos)
                self.advance()
                return token
            
            # if nothing matched, error
            self.error()
        
        # end of input
        return Token(TokenType.EOF, None, self.pos)
    
    def tokenize(self):
        # generate all tokens at once
        tokens = []
        
        try:
            token = self.get_next_token()
            
            while token.type != TokenType.EOF:
                tokens.append(token)
                token = self.get_next_token()
            
            tokens.append(token)  # append EOF token
        except Exception as e:
            # add basic err handling
            print(f"Tokenization failed: {e}")
            return []
            
        return tokens