from lexer import Lexer, TokenType, Token

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

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.curr_tok = self.tokens[0] if tokens else None
    
    def error(self, msg="Syntax error"):
        print(f"Error: {msg}")
        return None
    
    def eat(self, tok_type):
        if self.curr_tok and self.curr_tok.type == tok_type:
            tok = self.curr_tok
            self.pos += 1
            self.curr_tok = self.tokens[self.pos] if self.pos < len(self.tokens) else None
            return tok
        else:
            return self.error(f"Expected {tok_type}, got {self.curr_tok.type if self.curr_tok else 'None'}")
    
    def parse(self):
        #parsing with assignment rule
        if not self.tokens or len(self.tokens) <= 1:  # Only EOF token
            return None
            
        return self.assignment()
    
    def assignment(self):
        # assignment -> expr [= expr]
        expr = self.expr()
        
        if not expr:
            return None
        
        if self.curr_tok and self.curr_tok.type == TokenType.ASSIGNMENT:
            token = self.eat(TokenType.ASSIGNMENT)
            if not token:
                return None
                
            right = self.expr()
            if not right:
                return None
                
            if isinstance(expr, IdNode):
                return AssignNode(expr, right)
            else:
                return self.error("Left side of assignment must be identifier")
        
        return expr
    
    def expr(self):
        # expr -> term [(+|-) term]*
        node = self.term()
        
        if not node:
            return None
        
        while (self.curr_tok and 
               self.curr_tok.type == TokenType.OPERATOR and 
               self.curr_tok.value in ('+', '-')):
            
            op_tok = self.eat(TokenType.OPERATOR)
            if not op_tok:
                return None
                
            right = self.term()
            if not right:
                return None
                
            node = BinOpNode(node, op_tok.value, right)
        
        return node
    
    def term(self):
        # term -> factor [(*|/) factor]*
        node = self.factor()
        
        if not node:
            return None
        
        while (self.curr_tok and 
               self.curr_tok.type == TokenType.OPERATOR and 
               self.curr_tok.value in ('*', '/')):
            
            op_tok = self.eat(TokenType.OPERATOR)
            if not op_tok:
                return None
                
            right = self.factor()
            if not right:
                return None
                
            node = BinOpNode(node, op_tok.value, right)
        
        return node
    
    def factor(self):
        # factor -> NUMBER | IDENTIFIER | FUNCTION(expr) | (expr)
        if not self.curr_tok:
            return self.error("Unexpected end of input")
            
        if self.curr_tok.type == TokenType.NUMBER:
            token = self.eat(TokenType.NUMBER)
            if not token:
                return None
            return NumNode(token.value)
        
        elif self.curr_tok.type == TokenType.IDENTIFIER:
            token = self.eat(TokenType.IDENTIFIER)
            if not token:
                return None
            return IdNode(token.value)
        
        elif self.curr_tok.type == TokenType.FUNCTION:
            func_name = self.curr_tok.value
            token = self.eat(TokenType.FUNCTION)
            if not token:
                return None
            
            if not self.eat(TokenType.LPAREN):
                return None
            
            arg = self.expr()
            if not arg:
                return None
            
            if not self.eat(TokenType.RPAREN):
                return None
                
            return FuncCallNode(func_name, arg)
        
        elif self.curr_tok.type == TokenType.LPAREN:
            if not self.eat(TokenType.LPAREN):
                return None
            
            expr = self.expr()
            if not expr:
                return None
            
            if not self.eat(TokenType.RPAREN):
                return None
                
            return expr
        
        else:
            return self.error(f"Unexpected token: {self.curr_tok.type}")

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