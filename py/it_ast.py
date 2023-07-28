'''
AST 抽象语法树数据结构
Node 是所有的节点抽象

Program 程序根节点，由若干个表达式 Statement 组成

Statement 语句节点 语句类型 StatementType 及其枚举 StatementTypes
LetStatement LET-语句
ReturnStatement RETURN-语句
EmptyStatement 空语句，单个分号
ExpressionStatement 表达式语句。"x+10;" 是一个合法的语句

Expression 表达式节点 表达式类型 ExpressionType 及其枚举 ExpressionTypes
IdentifierNode 标识符节点，表达式的一种，但是也可以当作左值
IntegerLiteral 整数字面量
'''
from it_token import Token, TokenTypes, TokenType
from typing import List, Optional
import functools

class Node:
    '''
    AST 所有的节点抽象
    '''
    def tokens(self)->List[Token]:
        raise NotImplemented
    def __str__(self) -> str:
        return str(self.tokens())
    def __repr__(self) -> str:
        return str(self)

class StatementType(str):
    '''
    语句类型
    '''
    pass

class StatementTypes:
    '''
    语句类型枚举
    '''
    EMPTY = StatementType("EMPTY")
    LET = StatementType("LET")
    RETURN = StatementType("RETURN")
    EXPRESSION = StatementType("EXPRESSION")

class Statement(Node):
    '''
    所有语句节点的抽象
    '''
    def statementType(self)->StatementType:
        raise NotImplemented
    def asLetStatement(self)->'LetStatement':
        if isinstance(self, LetStatement):
            return self
        else:
            raise Exception(f"{self} is not LetStatement")
    def asReturnStatement(self)->'ReturnStatement':
        if isinstance(self, ReturnStatement):
            return self
        else:
            raise Exception(f"{self} is not ReturnStatement")
    def asExpression(self)->'Expression':
        if isinstance(self, Expression):
            return self
        else:
            raise Exception(f"{self} is not Expression")

class ExpressionType(str):
    '''
    表达式类型
    '''
    pass

class ExpressionTypes:
    '''
    表达式类型枚举
    '''
    IDENTIFIER = ExpressionType("IDENTIFIER") # 标识符表达式
    LITERAL = ExpressionType("LITERAL") # 字面量表达式
    PREFIX = ExpressionType("PREFIX") # 前缀表达式
    BINARY = ExpressionType("BINARY") # 二元运算表达式

class Expression(Node):
    '''
    所有表达式节点的抽象，表达式也是一个语句
    '''
    def expressionType(self)->ExpressionType:
        raise NotImplemented

class Program(Node):
    '''
    程序，AST 的根节点，由多个 statement 组成
    '''
    def __init__(self) -> None:
        super().__init__()
        self._statements:List[Statement] = []
    def addStatement(self, s:Statement)->None:
        self._statements.append(s)
    def statements(self)->List[Statement]:
        return self._statements
    def tokens(self)->List[Token]:
        return functools.reduce(lambda a,b:a+b, (s.tokens() for s in self.statements()))

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
    def expressionType(self)->ExpressionType:
        return ExpressionTypes.PREFIX
    def tokens(self)->List[Token]:
        return [self.prefixToken] + self.tokens()
    

class IdentifierNode(Expression):
    '''
    标识符节点，表达式的一种，但是也可以当作左值
    '''
    def __init__(self, t:Token) -> None:
        self.token = t.checkTokenType(TokenTypes.IDENTIFIER)
        super().__init__()
    def name(self)->str:
        return self.token.literal
    def expressionType(self)->ExpressionType:
        return ExpressionTypes.IDENTIFIER
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
    def expressionType(self)->ExpressionType:
        return ExpressionTypes.LITERAL
    def tokens(self)->List[Token]:
        return [self.token]

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
    def expressionType(self)->ExpressionType:
        return ExpressionTypes.BINARY
    def tokens(self)->List[Token]:
        return [Token(TokenTypes.L_PAREN)] +  self.left().tokens() + [self.operator()] + self.right().tokens() + [Token(TokenTypes.R_PAREN)]

class EmptyStatement(Statement):
    '''
    空语句
    '''
    def __init__(self) -> None:
        super().__init__()
    def statementType(self)->StatementType:
        return StatementTypes.EMPTY
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
    def statementType(self)->StatementType:
        return StatementTypes.EXPRESSION
    def tokens(self)->List[Token]: # let id = (expr);
        expr = self._expression.tokens()
        if expr[0].tokenType == TokenTypes.L_PAREN and expr[-1].tokenType == TokenTypes.R_PAREN:
            expr = expr[1:-1]
        return expr + [Token(TokenTypes.SEMICOLON)]

class LetStatement(Statement):
    '''
    LET 语句
    '''
    def __init__(self, identifier:IdentifierNode, expression:Expression) -> None:
        super().__init__()
        self._identifier = identifier
        self._expression = expression
    def statementType(self)->StatementType:
        return StatementTypes.LET
    def identifier(self)->IdentifierNode:
        return self._identifier
    def expression(self)->Expression:
        return self._expression
    def tokens(self)->List[Token]: # let id = (expr);
        return [Token(TokenTypes.KW_LET)] + self._identifier.tokens() \
              + [Token(TokenTypes.OP_ASSIGN)] + self._expression.tokens() + [Token(TokenTypes.SEMICOLON)]

class ReturnStatement(Statement):
    '''
    RETURN 语句
    '''
    def __init__(self, expression:Expression) -> None:
        super().__init__()
        self._expression = expression
    def statementType(self)->StatementType:
        return StatementTypes.RETURN
    def expression(self)->Expression:
        return self._expression
    def tokens(self)->List[Token]: # return (expr);
        return [Token(TokenTypes.KW_RETURN)] + self._expression.tokens() + [Token(TokenTypes.SEMICOLON)]