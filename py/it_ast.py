'''
AST 抽象语法树数据结构
Node 是所有的节点抽象

Block 代码块，由若干个表达式 Statement 组成
Program 程序根节点，即一个代码块

Statement 语句节点 语句类型 StatementType 及其枚举 StatementTypes
AssignStatement 赋值语句
LetStatement LET-语句
ReturnStatement RETURN-语句
IfStatement IF-语句 if (expt) {block} [else {block}]
WhileStatement WHILE-语句 while (expt) {block}
EmptyStatement 空语句，单个分号
ExpressionStatement 表达式语句。"x+10;" 是一个合法的语句


Expression 表达式节点 表达式类型 ExpressionType 及其枚举 ExpressionTypes
PrefixExpression 前缀表达式，前缀运算符加上表达式组成
BinaryOperatorExpression 二元运算表达式，由左右表达式和二元运算符组成
IdentifierNode 标识符节点，表达式的一种，但是也可以当作左值
BoolLiteral 布尔字面量
IntegerLiteral 整数字面量
FuncLiteral 函数字面量 fn(Identifier...){block}
FuncCaller 函数调用，包括普通的 id(expr...) 和立即函数 FuncLiteral(expr...)
'''
from it_token import Token, TokenTypes, TokenType
from typing import List, Union, TypeVar, Type
import functools

class NodeType(str):
    pass

class NodeTypes:
    EMPTY_STATEMENT = NodeType("EMPTY-STATEMENT")
    ASSIGN_STATEMENT = NodeType("ASSIGN-STATEMENT")
    LET_STATEMENT = NodeType("LET-STATEMENT")
    RETURN_STATEMENT = NodeType("RETURN-STATEMENT")
    EXPRESSION_STATEMENT = NodeType("EXPRESSION-STATEMENT")
    IF_STATEMENT = NodeType("IF-STATEMENT")
    WHILE_STATEMENT = NodeType("WHILE-STATEMENT")
    BLOCK_STATEMENT = NodeType("BLOCK-STATEMENT")

    IDENTIFIER_EXPRESSION = NodeType("IDENTIFIER-EXPRESSION") # 标识符表达式
    INTEGER_LITERAL_EXPRESSION = NodeType("INTEGER-LITERAL-EXPRESSION") # 字面量表达式
    BOOL_LITERAL_EXPRESSION = NodeType("BOOL-LITERAL-EXPRESSION") # 字面量表达式
    FUNC_LITERAL_EXPRESSION = NodeType("FUNC-LITERAL-EXPRESSION") # 函数字面量表达式
    PREFIX_EXPRESSION = NodeType("PREFIX-EXPRESSION") # 前缀表达式
    BINARY_EXPRESSION = NodeType("BINARY-EXPRESSION") # 二元运算表达式
    FUNC_CALLER_EXPRESSION = NodeType("FUNC-CALLER-EXPRESSION") # 函数调用表达式

class Node:
    T = TypeVar("T")
    '''
    AST 所有的节点抽象
    '''
    def tokens(self)->List[Token]:
        raise NotImplemented
    def nodeType(self)->NodeType:
        raise NotImplemented
    def __str__(self) -> str:
        return " ".join((t.__repr__() for t in self.tokens()))
    def __repr__(self) -> str:
        return str(self)
    def treatAs(self, hint:Type[T])->T: # ide-friendly
        if isinstance(self, hint):
            return self
        else:
            raise Exception(f"{self} is not a {hint.__name__}")


class Statement(Node):
    pass

class Expression(Node):
    pass

class Block(Statement):
    '''
    代码块
    '''
    def __init__(self) -> None:
        super().__init__()
        self._statements:List[Statement] = []
    def nodeType(self)->NodeType:
        return NodeTypes.BLOCK_STATEMENT
    def addStatement(self, s:Statement)->None:
        self._statements.append(s)
    def statements(self)->List[Statement]:
        return self._statements
    def tokens(self)->List[Token]:
        return [Token(TokenTypes.L_BRACE)] + functools.reduce(lambda a,b:a+b, (s.tokens() for s in self.statements()),[]) + [Token(TokenTypes.R_BRACE)]

class Program(Block):
    '''
    程序，AST 的根节点，就是一个代码块
    '''
    def __init__(self, block:Block) -> None:
        super().__init__()
        self._statements.extend(block.statements())
    def tokens(self)->List[Token]:
        return functools.reduce(lambda a,b:a+b, (s.tokens() for s in self.statements()),[])


class PrefixExpression(Expression):
    '''
    前缀表达式
    '''
    def __init__(self, prefixToken:Token, expression:Expression) -> None:
        super().__init__()
        self.prefixToken = prefixToken
        self._expression = expression
    def prefixType(self)->TokenType:
        return self.prefixToken.tokenType
    def rawExpression(self)->Expression:
        return self._expression
    def nodeType(self)->NodeType:
        return NodeTypes.PREFIX_EXPRESSION
    def tokens(self)->List[Token]:
        return [Token(TokenTypes.L_PAREN)] + [self.prefixToken] + self.rawExpression().tokens() + [Token(TokenTypes.R_PAREN)] 
    

class IdentifierNode(Expression):
    '''
    标识符节点，表达式的一种，但是也可以当作左值
    '''
    def __init__(self, t:Token) -> None:
        self.token = t.checkTokenType(TokenTypes.IDENTIFIER)
        super().__init__()
    def name(self)->str:
        return self.token.literal
    def nodeType(self)->NodeType:
        return NodeTypes.IDENTIFIER_EXPRESSION
    def tokens(self)->List[Token]:
        return [self.token]

class IntegerLiteral(Expression):
    '''
    整数字面量
    '''
    def __init__(self, token:Token) -> None:
        super().__init__()
        self.token = token.checkTokenType(TokenTypes.INTEGER)
    def integerValue(self)->int:
        return int(self.token.literal)
    def nodeType(self)->NodeType:
        return NodeTypes.INTEGER_LITERAL_EXPRESSION
    def tokens(self)->List[Token]:
        return [self.token]

class BoolLiteral(Expression):
    '''
    布尔字面量
    '''
    def __init__(self, token:Token) -> None:
        super().__init__()
        if token.tokenType != TokenTypes.KW_TRUE and token.tokenType != TokenTypes.KW_FALSE:
            raise Exception(f"{token} is not boolean")
        self.token = token
    def boolValue(self)->bool:
        return self.token.tokenType == TokenTypes.KW_TRUE
    def nodeType(self)->NodeType:
        return NodeTypes.BOOL_LITERAL_EXPRESSION
    def tokens(self)->List[Token]:
        return [self.token]
    
class FuncLiteral(Expression):
    '''
    函数字面量
    '''
    def __init__(self, identifiers:List[IdentifierNode], body:Block) -> None:
        super().__init__()
        self._parameters = identifiers
        self._body = body
    def nodeType(self)->NodeType:
        return NodeTypes.FUNC_LITERAL_EXPRESSION
    def parameters(self)->List[IdentifierNode]:
        return self._parameters
    def parameterNames(self)->List[str]:
        return [id.name() for id in self._parameters]
    def body(self)->Block:
        return self._body
    def tokens(self)->List[Token]:
        ts = [Token(TokenTypes.KW_FUNC), Token(TokenTypes.L_PAREN)] # fn(
        [ts.extend(id.tokens() + [Token(TokenTypes.COMMA)]) for id in self.parameters()] if len(self.parameters()) > 0 else None
        ts.pop() if len(self.parameters()) > 0 else None
        ts.append(Token(TokenTypes.R_PAREN)) # )
        ts.extend(self.body().tokens()) # block
        return ts


class FuncCaller(Expression):
    '''
    函数调用
    分为 IdentifierNode(expr...) 和 FuncLiteral(expr...) 两种
    '''
    def __init__(self, callee:Union[IdentifierNode, FuncLiteral], arguments:List[Expression]) -> None:
        super().__init__()
        self._callee = callee
        self._arguments = arguments
    def callee(self)->Union[IdentifierNode, FuncLiteral]:
        return self._callee
    def arguments(self)->List[Expression]:
        return self._arguments
    def nodeType(self)->NodeType:
        return NodeTypes.FUNC_CALLER_EXPRESSION
    def tokens(self)->List[Token]:
        ts = self.callee().tokens()
        ts.append(Token(TokenTypes.L_PAREN)) # (
        [ts.extend(a.tokens() + [Token(TokenTypes.COMMA)]) for a in self.arguments()] if len(self.arguments()) > 0 else None
        ts.pop() if len(self.arguments()) > 0 else None
        ts.append(Token(TokenTypes.R_PAREN)) # )
        return ts


class BinaryOperatorExpression(Expression):
    '''
    二元运算表达式
    '''
    def __init__(self, left:Expression, operator:Token, right:Expression) -> None:
        super().__init__()
        self._left = left
        self._operator = operator
        self._right = right
    def left(self)->Expression:
        return self._left
    def right(self)->Expression:
        return self._right
    def operator(self)->Token:
        return self._operator
    def operatorType(self)->TokenType:
        return self._operator.tokenType
    def nodeType(self)->NodeType:
        return NodeTypes.BINARY_EXPRESSION
    def tokens(self)->List[Token]:
        return [Token(TokenTypes.L_PAREN)] +  self.left().tokens() + [self.operator()] + self.right().tokens() + [Token(TokenTypes.R_PAREN)]

class EmptyStatement(Statement):
    '''
    空语句
    '''
    def __init__(self) -> None:
        super().__init__()
    def nodeType(self)->NodeType:
        return NodeTypes.EMPTY_STATEMENT
    def tokens(self)->List[Token]: # ;
        return [Token(TokenTypes.SEMICOLON)]

class ExpressionStatement(Statement):
    '''
    表达式语句
    '''
    def __init__(self, expression:Expression) -> None:
        super().__init__()
        self._expression = expression
    def expression(self)->Expression:
        return self._expression
    def nodeType(self)->NodeType:
        return NodeTypes.EXPRESSION_STATEMENT
    def tokens(self)->List[Token]: # let id = (expr);
        expr = self._expression.tokens()
        if expr[0].tokenType == TokenTypes.L_PAREN and expr[-1].tokenType == TokenTypes.R_PAREN:
            expr = expr[1:-1]
        return expr + [Token(TokenTypes.SEMICOLON)]

class AssignStatement(Statement):
    '''
    赋值语句
    '''
    def __init__(self, identifier:IdentifierNode, expression:Expression) -> None:
        super().__init__()
        self._identifier = identifier
        self._expression = expression
    def nodeType(self)->NodeType:
        return NodeTypes.ASSIGN_STATEMENT
    def identifier(self)->IdentifierNode:
        return self._identifier
    def expression(self)->Expression:
        return self._expression
    def tokens(self)->List[Token]: # id = (expr);
        expr = self._expression.tokens()
        if expr[0].tokenType == TokenTypes.L_PAREN and expr[-1].tokenType == TokenTypes.R_PAREN:
            expr = expr[1:-1]
        return self._identifier.tokens() + [Token(TokenTypes.OP_ASSIGN)] + expr + [Token(TokenTypes.SEMICOLON)]
    
class LetStatement(Statement):
    '''
    LET 语句
    '''
    def __init__(self, identifier:IdentifierNode, expression:Expression) -> None:
        super().__init__()
        self._identifier = identifier
        self._expression = expression
    def nodeType(self)->NodeType:
        return NodeTypes.LET_STATEMENT
    def identifier(self)->IdentifierNode:
        return self._identifier
    def expression(self)->Expression:
        return self._expression
    def tokens(self)->List[Token]: # let id = (expr);
        expr = self._expression.tokens()
        if expr[0].tokenType == TokenTypes.L_PAREN and expr[-1].tokenType == TokenTypes.R_PAREN:
            expr = expr[1:-1]
        return [Token(TokenTypes.KW_LET)] + self._identifier.tokens() \
              + [Token(TokenTypes.OP_ASSIGN)] + expr + [Token(TokenTypes.SEMICOLON)]

class ReturnStatement(Statement):
    '''
    RETURN 语句
    '''
    def __init__(self, expression:Expression) -> None:
        super().__init__()
        self._expression = expression
    def nodeType(self)->NodeType:
        return NodeTypes.RETURN_STATEMENT
    def expression(self)->Expression:
        return self._expression
    def tokens(self)->List[Token]: # return (expr);
        expr = self._expression.tokens()
        if expr[0].tokenType == TokenTypes.L_PAREN and expr[-1].tokenType == TokenTypes.R_PAREN:
            expr = expr[1:-1]
        return [Token(TokenTypes.KW_RETURN)] + expr + [Token(TokenTypes.SEMICOLON)]
    
class IfStatement(Statement):
    '''
    IF 语句 if (expt) {block} [else {block}]
    else 可选
    '''
    def __init__(self, condition:Expression, consequence:Block, alternative:Block) -> None:
        super().__init__()
        self._condition = condition
        self._consequence = consequence
        self._alternative = alternative
    def nodeType(self)->NodeType:
        return NodeTypes.IF_STATEMENT
    def condition(self)->Expression:
        return self._condition
    def consequence(self)->Block:
        return self._consequence
    def alternative(self)->Block:
        return self._alternative
    def tokens(self)->List[Token]: # if (expr) {block} else {block}
        cond = self.condition().tokens()
        if cond[0].tokenType == TokenTypes.L_PAREN and cond[-1].tokenType == TokenTypes.R_PAREN:
            cond = cond[1:-1]

        ts = [Token(TokenTypes.KW_IF), Token(TokenTypes.L_PAREN)] # if(
        ts.extend(cond) # expr
        ts.append(Token(TokenTypes.R_PAREN)) # )
        ts.extend(self.consequence().tokens()) # block
        ts.append(Token(TokenTypes.KW_ELSE)) # else
        ts.extend(self.alternative().tokens()) # block
        return ts

class WhileStatement(Statement):
    def __init__(self, condition:Expression, body:Block) -> None:
        super().__init__()
        self._condition = condition
        self._body = body
    def nodeType(self)->NodeType:
        return NodeTypes.WHILE_STATEMENT
    def condition(self)->Expression:
        return self._condition
    def body(self)->Block:
        return self._body
    def tokens(self)->List[Token]: # while (expr) {block}
        cond = self.condition().tokens()
        if cond[0].tokenType == TokenTypes.L_PAREN and cond[-1].tokenType == TokenTypes.R_PAREN:
            cond = cond[1:-1]

        ts = [Token(TokenTypes.KW_WHILE), Token(TokenTypes.L_PAREN)] # while(
        ts.extend(cond) # expr
        ts.append(Token(TokenTypes.R_PAREN)) # )
        ts.extend(self.body().tokens()) # block
        return ts
    
if __name__ == "__main__":
    node:Node = IntegerLiteral(Token(TokenTypes.INTEGER, "123"))
    print(node, node.treatAs(IntegerLiteral).integerValue())

    try:
        node.treatAs(WhileStatement)
    except Exception as e:
        print(e)
