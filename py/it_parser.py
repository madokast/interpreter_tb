'''
parser 语法分析
Syntax analysis (also known as parsing) involves parsing the token sequence to identify the syntactic structure of the program.
词法分析，或 parsing，将 token 序列转为语法结构
'''
from it_tokenizer import Tokenizer, SourceReader
from it_token import Token, TokenTypes
from it_ast import *
from it_precidence import Precidence
from queue import Queue
from typing import Optional
import io


class Parser:
    def __init__(self, tokenizer:Tokenizer) -> None:
        self.tokenizer = tokenizer
        self.queue:Queue[Token] = Queue()
    def nextToken(self)->Token: # 读下一个 token
        return self.tokenizer.nextToken() if self.queue.empty() else self.queue.get()
    def unreadToken(self, t:Token)->None: # 放入 token
        self.queue.put(t)
    def topToken(self)->Token: # 查看下一个 token 不读出
        t = self.nextToken()
        self.unreadToken(t)
        return t
    def parse(self)->Program:
        program = Program()
        while self.topToken().tokenType != TokenTypes.EOF: # topToken 不是 EOF
            if self.topToken().tokenType == TokenTypes.KW_LET: # 解析 LET 语句
                program.addStatement(self.parseLetStatement())
            elif self.topToken().tokenType == TokenTypes.KW_RETURN: # 解析 RETURN 语句
                program.addStatement(self.parseReturnStatement())
            elif self.topToken().tokenType == TokenTypes.SEMICOLON: # 空语句
                program.addStatement(self.parseEmptyStatement())
            else: # 表达式语句
                program.addStatement(self.parseExpressionStatement())
        return program
    def parseEmptyStatement(self)->EmptyStatement:
        semicolumnToken = self.nextToken().checkTokenType(TokenTypes.SEMICOLON)
        return EmptyStatement()
    def parseExpressionStatement(self)->ExpressionStatement:
        expression = self.parseExpression(Precidence.LOWEST)
        semicolumnToken = self.nextToken().checkTokenType(TokenTypes.SEMICOLON)
        return ExpressionStatement(expression)
    def parseLetStatement(self)->LetStatement:
        letToken = self.nextToken().checkTokenType(TokenTypes.KW_LET)
        identifierToken = self.nextToken().checkTokenType(TokenTypes.IDENTIFIER)
        assignToken = self.nextToken().checkTokenType(TokenTypes.OP_ASSIGN)
        expression = self.parseExpression(Precidence.LOWEST)
        semicolumnToken = self.nextToken().checkTokenType(TokenTypes.SEMICOLON)
        return LetStatement(IdentifierNode(identifierToken), expression)
    def parseReturnStatement(self)->ReturnStatement:
        returnToken = self.nextToken().checkTokenType(TokenTypes.KW_RETURN)
        expression = self.parseExpression(Precidence.LOWEST)
        semicolumnToken = self.nextToken().checkTokenType(TokenTypes.SEMICOLON)
        return ReturnStatement(expression)
    def parseExpression(self, curPrecidence:int)->Expression:
        '''
        解析表达式
        '''
        # 首先解析出左操作数
        left = self.parseLeftOprand()
        # 然后组装二元运算符，注意只有优先级高才组合
        while self.topToken().tokenType != TokenTypes.SEMICOLON and Precidence.of(self.topToken().tokenType) > curPrecidence:
            operator = self.nextToken()
            left = BinaryOperatorExpression(left, operator, self.parseExpression(Precidence.of(operator.tokenType)))
        return left
    def parseLeftOprand(self)->Expression:
        '''
        解析左操作数
        '''
        firstToken = self.nextToken()
        if firstToken.tokenType == TokenTypes.OP_MINUS or firstToken.tokenType == TokenTypes.OP_MINUS:
            return PrefixExpression(firstToken, self.parseLeftOprand())
        else:
            if firstToken.tokenType == TokenTypes.INTEGER:
                return IntegerLiteral(firstToken)
            elif firstToken.tokenType == TokenTypes.IDENTIFIER:
                return IdentifierNode(firstToken)
            else:
                raise Exception(f"unexcept token {firstToken}")


if __name__ == "__main__":
    def parser(code:str)->None:
        print(f"\n>>> {code}")
        sr = SourceReader(io.BytesIO(code.encode("ascii")))
        tn = Tokenizer(sr)
        parser = Parser(tn)
        program = parser.parse()
        for s in program.statements():
            print(s.statementType(), s.tokens())

    parser("let a = 5; let b = 838383; let c = a;")
    parser("return a; return 838383;")
    parser("a; 838383; ;; ")
    parser("1;")
    parser("1+2;")
    parser("1+2+3;")
    parser("1+2*3;")
    parser("1+2*3+4;")
    parser("a+233==356+ccc;")

    

