from lexer import Lexer, TokenType, Token

# AST node cl
class ASTNode:
    pass

class NumNode(ASTNode):
    def __init__(self, val):
        self.val = val
    
    def __str__(self):
        return f"Num({self.val})"

class IdNode(ASTNode):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return f"Id({self.name})"

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __str__(self):
        return f"BinOp({self.op}, {self.left}, {self.right})"

class FuncCallNode(ASTNode):
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg
    
    def __str__(self):
        return f"FuncCall({self.name}, {self.arg})"

class AssignNode(ASTNode):
    def __init__(self, id_node, expr):
        self.id_node = id_node
        self.expr = expr
    
    def __str__(self):
        return f"Assign({self.id_node}, {self.expr})"

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.curr_tok = self.tokens[0] if tokens else None
    
    def err(self, expected=None):
        if not self.curr_tok:
            raise ParserError("Unexpected end of input")
        
        tok = self.curr_tok
        msg = f"Syntax error at pos {tok.position}: got {tok.type}"
        if tok.value is not None:
            msg += f" '{tok.value}'"
        if expected:
            msg += f", expected {expected}"
        raise ParserError(msg)
    
    def eat(self, tok_type):
        if not self.curr_tok:
            self.err(f"{tok_type}")
            
        if self.curr_tok.type == tok_type:
            tok = self.curr_tok
            self.pos += 1
            self.curr_tok = self.tokens[self.pos] if self.pos < len(self.tokens) else None
            return tok
        else:
            self.err(f"{tok_type}")
    
    def parse(self):
        if not self.tokens or len(self.tokens) <= 1:  # Only EOF token
            return None
        
        try:
            #parsing from highest level rule
            return self.assignment()
        except ParserError as e:
            print(f"Parser error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def assignment(self):
        """Rule: assignment -> expr [= expr]"""
        expr = self.expr()
        
        # heck for assgn operator
        if self.curr_tok and self.curr_tok.type == TokenType.ASSIGNMENT:
            self.eat(TokenType.ASSIGNMENT)
            right = self.expr()
            
            if isinstance(expr, IdNode):
                return AssignNode(expr, right)
            else:
                self.err("identifier on left side of assignment")
        
        return expr
    
    def expr(self):
        """Rule: expr -> term [(+|-) term]*"""
        node = self.term()
        
        while (self.curr_tok and 
               self.curr_tok.type == TokenType.OPERATOR and 
               self.curr_tok.value in ('+', '-')):
            op = self.eat(TokenType.OPERATOR).value
            node = BinOpNode(node, op, self.term())
        
        return node
    
    def term(self):
        """Rule: term -> factor [(*|/) factor]*"""
        node = self.factor()
        
        while (self.curr_tok and 
               self.curr_tok.type == TokenType.OPERATOR and 
               self.curr_tok.value in ('*', '/')):
            op = self.eat(TokenType.OPERATOR).value
            node = BinOpNode(node, op, self.factor())
        
        return node
    
    def factor(self):
        """Rule: factor -> NUMBER | IDENTIFIER | FUNCTION(expr) | (expr)"""
        if not self.curr_tok:
            self.err("factor")
            
        tok = self.curr_tok
        
        if tok.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumNode(tok.value)
        
        elif tok.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return IdNode(tok.value)
        
        elif tok.type == TokenType.FUNCTION:
            func_name = tok.value
            self.eat(TokenType.FUNCTION)
            
            try:
                self.eat(TokenType.LPAREN)
                arg = self.expr()
                self.eat(TokenType.RPAREN)
                return FuncCallNode(func_name, arg)
            except ParserError:
                raise ParserError(f"Invalid function call syntax for '{func_name}' at position {tok.position}")
        
        elif tok.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            
            try:
                self.eat(TokenType.RPAREN)
                return node
            except ParserError:
                raise ParserError(f"Missing closing parenthesis for opening parenthesis at position {tok.position}")
        
        else:
            self.err("NUMBER, IDENTIFIER, FUNCTION or (")

def print_ast(node, lvl=0):
    if node is None:
        return
        
    indent = '  ' * lvl
    
    if isinstance(node, NumNode):
        print(f"{indent}Num: {node.val}")
    elif isinstance(node, IdNode):
        print(f"{indent}Id: {node.name}")
    elif isinstance(node, BinOpNode):
        print(f"{indent}BinOp: {node.op}")
        print(f"{indent}  Left:")
        print_ast(node.left, lvl + 2)
        print(f"{indent}  Right:")
        print_ast(node.right, lvl + 2)
    elif isinstance(node, FuncCallNode):
        print(f"{indent}FuncCall: {node.name}")
        print(f"{indent}  Arg:")
        print_ast(node.arg, lvl + 2)
    elif isinstance(node, AssignNode):
        print(f"{indent}Assign:")
        print(f"{indent}  Target:")
        print_ast(node.id_node, lvl + 2)
        print(f"{indent}  Value:")
        print_ast(node.expr, lvl + 2)