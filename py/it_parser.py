'''
parser 语法分析
Syntax analysis (also known as parsing) involves parsing the token sequence to identify the syntactic structure of the program.
词法分析，或 parsing，将 token 序列转为语法结构
'''
from it_tokenizer import Tokenizer, SourceReader
from it_token import Token, TokenTypes
from it_ast import Program, LetStatement, Expression, IdentifierNode, IntegerLiteral
from queue import Queue
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
        while self.topToken().tokenType != TokenTypes.EOF:
            if self.topToken().tokenType == TokenTypes.KW_LET:
                program.addStatement(self.parseLetStatement())
            # TODO
        return program
    def parseLetStatement(self)->LetStatement:
        letToken = self.nextToken().checkTokenType(TokenTypes.KW_LET)
        identifierToken = self.nextToken().checkTokenType(TokenTypes.IDENTIFIER)
        assignToken = self.nextToken().checkTokenType(TokenTypes.OP_ASSIGN)
        expression = self.parseExpression()
        semicolumnToken = self.nextToken().checkTokenType(TokenTypes.SEMICOLON)
        return LetStatement(IdentifierNode(identifierToken), expression)
    def parseExpression(self)->Expression:
        firstToken = self.nextToken()
        topToken = self.topToken()
        if topToken.tokenType == TokenTypes.SEMICOLON:
            if firstToken.tokenType == TokenTypes.INTEGER:
                return IntegerLiteral(firstToken)
        raise

if __name__ == "__main__":
    sr = SourceReader(io.BytesIO(b"let a = 5;"))
    tn = Tokenizer(sr)
    parser = Parser(tn)
    program = parser.parse()
    print(program.tokens())

