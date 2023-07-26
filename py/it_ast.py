'''
AST 抽象语法树数据结构
Node 是所有的节点抽象

Program 程序根节点，由若干个表达式 Statement 组成

Statement 语句节点 语句类型 StatementType 及其枚举 StatementTypes
LetStatement LET-语句

Expression 表达式节点 表达式类型 ExpressionType 及其枚举 ExpressionTypes
IdentifierNode 标识符节点，表达式的一种，但是也可以当作左值
IntegerLiteral 整数字面量
'''
from it_token import Token, TokenTypes
from typing import List
import functools

class Node:
    '''
    AST 所有的节点抽象
    '''
    def tokens(self)->List[Token]:
        raise NotImplemented
    def __str__(self) -> str:
        return str(self.tokens())

class StatementType(str):
    '''
    语句类型
    '''
    pass

class StatementTypes:
    '''
    语句类型枚举
    '''
    LET = StatementType("let")
    RETURN = StatementType("return")

class Statement(Node):
    '''
    所有语句节点的抽象
    '''
    def statementType(self)->StatementType:
        raise NotImplemented

class ExpressionType(str):
    '''
    表达式类型
    '''
    pass

class ExpressionTypes:
    IDENTIFIER = ExpressionType("identifier") # 标识符表达式
    LITERAL = ExpressionType("literal") # 字面量表达式

class Expression(Node):
    '''
    所有表达式节点的抽象
    '''
    def expressionType(self)->ExpressionType:
        raise NotImplemented

class Program(Node):
    def __init__(self) -> None:
        super().__init__()
        self._statements:List[Statement] = []
    def addStatement(self, s:Statement)->None:
        self._statements.append(s)
    def statements(self)->List[Statement]:
        return self._statements
    def tokens(self)->List[Token]:
        return functools.reduce(lambda a,b:a+b, (s.tokens() for s in self.statements()))

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

class LetStatement(Statement):
    def __init__(self, identifier:IdentifierNode, experssion:Expression) -> None:
        super().__init__()
        self._identifier = identifier
        self._experssion = experssion
    def tokens(self)->List[Token]: # let id = (expr);
        return [Token(TokenTypes.KW_LET)] + self._identifier.tokens() \
              + [Token(TokenTypes.OP_ASSIGN)] + self._experssion.tokens() + [Token(TokenTypes.SEMICOLON)]