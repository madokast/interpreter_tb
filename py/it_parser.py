'''
parser 语法分析
Syntax analysis (also known as parsing) involves parsing the token sequence to identify the syntactic structure of the program.
词法分析，或 parsing，将 token 序列转为语法结构
'''
from it_tokenizer import Tokenizer, SourceReader
from it_token import Token, TokenTypes
from it_ast import *
from it_prority import Prority
from queue import Queue

class parser:
    @staticmethod
    def isPrefixOperator(token:Token)->bool: # 是否前缀运算符 -/!
        return token.tokenType == TokenTypes.OP_MINUS or token.tokenType == TokenTypes.OP_BANG
    

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
        semicolumnToken = self.nextToken().checkTokenType(TokenTypes.SEMICOLON) # 要求下一 token 是分号
        return EmptyStatement()
    def parseExpressionStatement(self)->ExpressionStatement: # 解析表达式，之后接分号
        expression = self.parseExpression(Prority.LOWEST)
        semicolumnToken = self.nextToken().checkTokenType(TokenTypes.SEMICOLON)
        return ExpressionStatement(expression)
    def parseLetStatement(self)->LetStatement: # 解析 LET 语句 "let id = expr;"
        letToken = self.nextToken().checkTokenType(TokenTypes.KW_LET)
        identifierToken = self.nextToken().checkTokenType(TokenTypes.IDENTIFIER)
        assignToken = self.nextToken().checkTokenType(TokenTypes.OP_ASSIGN)
        expression = self.parseExpression(Prority.LOWEST)
        semicolumnToken = self.nextToken().checkTokenType(TokenTypes.SEMICOLON)
        return LetStatement(IdentifierNode(identifierToken), expression)
    def parseReturnStatement(self)->ReturnStatement: # 解析 RETURN 语句 "return expr;"
        returnToken = self.nextToken().checkTokenType(TokenTypes.KW_RETURN)
        expression = self.parseExpression(Prority.LOWEST)
        semicolumnToken = self.nextToken().checkTokenType(TokenTypes.SEMICOLON)
        return ReturnStatement(expression)
    def parseExpression(self, currentPriority:int)->Expression: # 解析表达式
        # 首先解析出左操作数
        left = self.parseLeftOprand()
        # 然后组装二元运算符，注意只有优先级高才组合
        while self.topToken().tokenType != TokenTypes.SEMICOLON and Prority.of(self.topToken().tokenType) > currentPriority:
            operator = self.nextToken()
            left = BinaryOperatorExpression(left, operator, self.parseExpression(Prority.of(operator.tokenType)))
        return left
    def parseLeftOprand(self)->Expression: # 解析左操作数
        firstToken = self.nextToken()
        # 判断是否有前缀运算符
        if parser.isPrefixOperator(firstToken):
            return PrefixExpression(firstToken, self.parseLeftOprand())
        else:
            if firstToken.tokenType == TokenTypes.INTEGER: # 整数字面量
                return IntegerLiteral(firstToken)
            elif firstToken.tokenType == TokenTypes.KW_TRUE or firstToken.tokenType == TokenTypes.KW_FALSE: # true/false 字面量
                return BoolLiteral(firstToken)
            elif firstToken.tokenType == TokenTypes.IDENTIFIER: # 标识符
                if self.topToken().tokenType == TokenTypes.L_PAREN: # 函数相关
                    raise Exception("impl for func")
                else:
                    return IdentifierNode(firstToken) # 非函数，仅仅是标识符
            elif firstToken.tokenType == TokenTypes.L_PAREN: # 左括号 (
                expr = self.parseExpression(Prority.LOWEST)
                rightParen = self.nextToken().checkTokenType(TokenTypes.R_PAREN)
                return expr
            else:
                raise Exception(f"unexcept token {firstToken}")




if __name__ == "__main__":
    import io
    def parse(code:str)->None:
        print(f"\n>>> {code}")
        sr = SourceReader(io.BytesIO(code.encode("ascii")))
        tn = Tokenizer(sr)
        parser = Parser(tn)
        program = parser.parse()
        print(program)
        if len(program.statements()) > 1:
            for s in program.statements():
                print(s.statementType(), s.tokens())

    parse("let a = 5; let b = 838383; let c = a;")
    parse("return a; return 838383;")
    parse("a; 838383; ;; ")
    parse("1;")
    parse("1+2;")
    parse("1+2+3;")
    parse("1+2*3;")
    parse("1+2*3+4;")
    parse("a+233==356+ccc;")
    parse("!true + false;")
    parse("let a = 3 < 5 == true;")
    parse("let a = (-1+-2)*(-5/(-6--7));")

    

