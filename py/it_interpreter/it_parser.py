'''
parser 语法分析
Syntax analysis (also known as parsing) involves parsing the token sequence to identify the syntactic structure of the program.
词法分析，或 parsing，将 token 序列转为语法结构
'''
from it_interpreter.it_tokenizer import Tokenizer, SourceReader
from it_interpreter.it_token import Token, TokenTypes
from it_interpreter.it_ast import *
from it_interpreter.it_prority import Priority
from typing import Union, List
from queue import Queue
import io

class parser:
    @staticmethod
    def isPrefixOperator(token:Token)->bool: # 是否前缀运算符 -/!
        return token.tokenType == TokenTypes.OP_MINUS or token.tokenType == TokenTypes.OP_BANG
    @staticmethod
    def parse(input:io.IOBase)->Program:
        sr = SourceReader(input)
        tn = Tokenizer(sr)
        ps = Parser(tn)
        return ps.parse()
    

class Parser:
    def __init__(self, tokenizer:Tokenizer) -> None:
        self.tokenizer = tokenizer
        self.unreadStack:List[Token] = []
        self.TailQueue:Queue[Token] = Queue()
    def nextToken(self)->Token: # 读下一个 token
        next = self.tokenizer.nextToken() if len(self.unreadStack)==0 else self.unreadStack.pop()
        if next.tokenType == TokenTypes.EOF and (not self.TailQueue.empty()):
            next = self.TailQueue.get()
        return next
    def unreadToken(self, t:Token)->None: # 放入 token
        self.unreadStack.append(t)
    def topToken(self)->Token: # 查看下一个 token 不读出
        t = self.nextToken()
        self.unreadToken(t)
        return t
    def tailAppend(self, token:Token)->None:
        self.TailQueue.put(token)
    def parse(self)->Program: # 解析程序
        self.unreadToken(Token(TokenTypes.L_BRACE))
        self.tailAppend(Token(TokenTypes.R_BRACE))
        program = Program(self.parseBlock())
        eofToken = self.nextToken().checkTokenType(TokenTypes.EOF)
        return program
    def parseBlock(self)->Block:
        leftBraceToken = self.nextToken().checkTokenType(TokenTypes.L_BRACE)
        block = Block()
        while self.topToken().tokenType != TokenTypes.R_BRACE: # topToken 不是右大括号 }
            if self.topToken().tokenType == TokenTypes.KW_LET: # 解析 LET 语句
                block.addStatement(self.parseLetStatement())
            elif self.topToken().tokenType == TokenTypes.KW_RETURN: # 解析 RETURN 语句
                block.addStatement(self.parseReturnStatement())
            elif self.topToken().tokenType == TokenTypes.KW_IF: # 解析 IF 语句
                block.addStatement(self.parseIfStatement())
            elif self.topToken().tokenType == TokenTypes.KW_WHILE: # 解析 IF 语句
                block.addStatement(self.parseWhileStatement())                
            elif self.topToken().tokenType == TokenTypes.L_BRACE: # 解析 block 语句
                block.addStatement(self.parseBlock())
            elif self.topToken().tokenType == TokenTypes.SEMICOLON: # 空语句
                block.addStatement(self.parseEmptyStatement())
            elif self.topToken().tokenType == TokenTypes.IDENTIFIER: # 赋值语句
                identifierToken = self.nextToken().checkTokenType(TokenTypes.IDENTIFIER)
                if self.topToken().tokenType == TokenTypes.OP_ASSIGN: 
                    self.unreadToken(identifierToken)
                    block.addStatement(self.parseAssignStatement())
                else: # 表达式语句
                    self.unreadToken(identifierToken)
                    block.addStatement(self.parseExpressionStatement())
            else: # 表达式语句
                block.addStatement(self.parseExpressionStatement())
        rightBraceToken = self.nextToken().checkTokenType(TokenTypes.R_BRACE)
        return block
    def parseEmptyStatement(self)->EmptyStatement:
        semicolumnToken = self.nextToken().checkTokenType(TokenTypes.SEMICOLON) # 要求下一 token 是分号
        return EmptyStatement()
    def parseExpressionStatement(self)->ExpressionStatement: # 解析表达式，之后接分号
        expression = self.parseExpression(Priority.LOWEST)
        semicolumnToken = self.nextToken().checkTokenType(TokenTypes.SEMICOLON)
        return ExpressionStatement(expression)
    def parseAssignStatement(self)->AssignStatement: # 解析赋值语句 id = expr;
        identifierToken = self.nextToken().checkTokenType(TokenTypes.IDENTIFIER)
        assignToken = self.nextToken().checkTokenType(TokenTypes.OP_ASSIGN)
        expression = self.parseExpression(Priority.LOWEST)
        semicolumnToken = self.nextToken().checkTokenType(TokenTypes.SEMICOLON)
        return AssignStatement(IdentifierNode(identifierToken), expression)
    def parseLetStatement(self)->LetStatement: # 解析 LET 语句 "let id = expr;"
        letToken = self.nextToken().checkTokenType(TokenTypes.KW_LET)
        assign = self.parseAssignStatement()
        return LetStatement(assign.identifier(), assign.expression())
    def parseReturnStatement(self)->ReturnStatement: # 解析 RETURN 语句 "return expr;"
        returnToken = self.nextToken().checkTokenType(TokenTypes.KW_RETURN)
        expression = self.parseExpression(Priority.LOWEST)
        semicolumnToken = self.nextToken().checkTokenType(TokenTypes.SEMICOLON)
        return ReturnStatement(expression)
    def parseIfStatement(self)->IfStatement: # 解析 IF 语句 "if(expt){block}else{block}"
        ifToken = self.nextToken().checkTokenType(TokenTypes.KW_IF)
        condition = self.parseExpression(Priority.LOWEST)
        consequence = self.parseBlock()
        alternative = Block()
        if self.topToken().tokenType == TokenTypes.KW_ELSE:
            elseToken = self.nextToken().checkTokenType(TokenTypes.KW_ELSE)
            alternative = self.parseBlock()
        return IfStatement(condition, consequence, alternative)
    def parseWhileStatement(self)->WhileStatement: # 解析 WHILE 语句 "while(expt){block}"
        whileToken = self.nextToken().checkTokenType(TokenTypes.KW_WHILE)
        condition = self.parseExpression(Priority.LOWEST)
        body = self.parseBlock()
        return WhileStatement(condition, body)
    def parseFuncCall(self)->FuncCaller: # 解析函数调用
        identifierToken = self.nextToken().checkTokenType(TokenTypes.IDENTIFIER) # 读标识符
        return FuncCaller(IdentifierNode(identifierToken), self.parseFuncArguments()) # 读实参列表
    def parseFuncArguments(self)->List[Expression]: # 解析函数实参 (expr...)
        leftParenToken = self.nextToken().checkTokenType(TokenTypes.L_PAREN) # 读到 (
        arguments:List[Expression] = [] # 实参
        if self.topToken().tokenType == TokenTypes.R_PAREN: # 马上读到 )，说明没有实参
            rightParenToken = self.nextToken().checkTokenType(TokenTypes.R_PAREN)
            return []
        else: # 说明存在实参
            while True:
                arguments.append(self.parseExpression(Priority.LOWEST)) # 读一个表达式
                if self.topToken().tokenType == TokenTypes.R_PAREN: # 读到 )，实参读完
                    rightParenToken = self.nextToken().checkTokenType(TokenTypes.R_PAREN)
                    return arguments
                else: # 读一个逗号 , 继续循环
                    commaToken = self.nextToken().checkTokenType(TokenTypes.COMMA)
    def parseFunction(self)->Union[FuncLiteral, FuncCaller]:
        funcToken = self.nextToken().checkTokenType(TokenTypes.KW_FUNC)
        leftParenToken = self.nextToken().checkTokenType(TokenTypes.L_PAREN)
        identifiers:List[IdentifierNode] = [] # 形参
        while self.topToken().tokenType == TokenTypes.IDENTIFIER:
            identifiers.append(IdentifierNode(self.nextToken().checkTokenType(TokenTypes.IDENTIFIER)))
            if self.topToken().tokenType == TokenTypes.R_PAREN:
                break
            commaToken = self.nextToken().checkTokenType(TokenTypes.COMMA)
        rightParenToken = self.nextToken().checkTokenType(TokenTypes.R_PAREN)
        body = self.parseBlock() # 读函数体
        if self.topToken().tokenType == TokenTypes.L_PAREN: # 读到 (，说明是立即函数
            return FuncCaller(FuncLiteral(identifiers, body), self.parseFuncArguments())
        else:
            return FuncLiteral(identifiers, body)
    def parseExpression(self, currentPriority:int)->Expression: # 解析表达式
        # 首先解析出左操作数
        left = self.parseLeftOprand()
        # 然后组装二元运算符，注意只有优先级高才组合
        while Priority.of(self.topToken().tokenType) > currentPriority:
            operator = self.nextToken()
            left = BinaryOperatorExpression(left, operator, self.parseExpression(Priority.of(operator.tokenType)))
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
                if self.topToken().tokenType == TokenTypes.L_PAREN: # 函数调用
                    self.unreadToken(firstToken)
                    return self.parseFuncCall()
                else:
                    return IdentifierNode(firstToken) # 非函数，仅仅是标识符
            elif firstToken.tokenType == TokenTypes.KW_FUNC: # 函数字面量 fn(){} 或者是立即函数 fn(){}()
                self.unreadToken(firstToken)
                return self.parseFunction()
            elif firstToken.tokenType == TokenTypes.L_PAREN: # 左括号 (
                expr = self.parseExpression(Priority.LOWEST)
                rightParen = self.nextToken().checkTokenType(TokenTypes.R_PAREN)
                return expr
            else:
                raise Exception(f"unexcept token {firstToken}")




if __name__ == "__main__":
    import io
    def _parse(code:str)->None:
        print(f"\n>>> {code}")
        sr = SourceReader(io.BytesIO(code.encode("ascii")))
        tn = Tokenizer(sr)
        parser = Parser(tn)
        program = parser.parse()
        print(program)
        if len(program.statements()) > 1:
            for s in program.statements():
                print(s.nodeType(), s.tokens())

    _parse("let a = 5; let b = 838383; let c = a;")
    _parse("return a; return 838383;")
    _parse("a; 838383; ;; ")
    _parse("1;")
    _parse("1+2;")
    _parse("1+2+3;")
    _parse("1+2*3;")
    _parse("1+2*3+4;")
    _parse("a+233==356+ccc;")
    _parse("!true + false;")
    _parse("let a = 3 < 5 == true;")
    _parse("let a = (-1+-2)*(-5/(-6--7));")
    _parse("{}{let a=1;let b=a;}{}")
    _parse("if(true){;}")
    _parse("if(a>b){return 1+2-3;}else{1+2*3;}")
    _parse("fn(a, b) {return a + b;};")
    _parse("let add = fn(a, b) {return a + b;};")
    _parse("fn(a, b) {return a + b;} (1, 2);")
    _parse("return 123 + a * fn(a, b) {return a + b;} (1, 1+2/3);")
    _parse("return 123 + a * fn(a, b) {return a + b;} (fn(){return 1;}(), 1+2/3);")
    _parse("let result = adder(1, 2);")
    _parse("return 123 + a * fn(a, b) {return a + b;} (fn(){return 1;}(), adder(3, 4));")
    _parse("let a = 0; while (a<100) {a=a+1;} return a;")
    
    

