from it_token import TokenType, Token, KeywordMap
import io
from queue import Queue
from typing import Dict, List


class tokenizer:
    char = str
    EOF = ""
    whitespaceSet = {" ", "\t", "\n", "\r"}
    @staticmethod
    def isWhitespace(c:char)->bool:
        return c in tokenizer.whitespaceSet
    @staticmethod
    def isLetter(c:char)->bool:
        return c.isupper() or c.islower()
    @staticmethod
    def isDigit(c:char)->bool:
        return c.isdigit()
    @staticmethod
    def tokenize(input:io.IOBase)->List[Token]:
        tokens = []
        sr = SourceReader(input)
        tk = Tokenizer(sr)
        while True:
            t = tk.nextToken()
            tokens.append(t)
            if t.tokenType == TokenType.EOF or t.tokenType == TokenType.ILLEGAL:
                return tokens

class SourceReader:
    '''
    原代码读取器
    read() 读取一个字符或返回 EOF
    unread(char) 放回一个字符
    '''

    def __init__(self, input:io.IOBase) -> None:
        self.input = input
        self.unreadBuf:Queue[tokenizer.char] = Queue()
    def read(self) -> tokenizer.char:
        if self.unreadBuf.empty():
            b = self.input.readline(1) # 读一个字符，读不到返回空
            return b.decode("ascii")
        else:
            return self.unreadBuf.get() # dequeue
    def readSkipWhitespace(self) -> tokenizer.char: # 读跳过空白
        c = self.read()
        while tokenizer.isWhitespace(c):
            c = self.read()
        return c
    def unread(self, c:tokenizer.char)->None: # 读多了写回
        self.unreadBuf.put(c) # inqueue
    def top(self)->tokenizer.char: # 查看
        c = self.read()
        self.unread(c)
        return c
    def readWord(self, fisrt:tokenizer.char)->str:
        word = str(fisrt)
        while True:
            c = self.read()
            if tokenizer.isLetter(c):
                word += str(c)
            else:
                self.unread(c)
                return word
    def readInteger(self, fisrt:tokenizer.char)->str:
        interger = str(fisrt)
        while True:
            c = self.read()
            if tokenizer.isDigit(c):
                interger += str(c)
            else:
                self.unread(c)
                return str(int(interger))

class Tokenizer:
    '''
    词法分析器
    '''
    def __init__(self, sr:SourceReader) -> None:
        self.sr = sr
    def nextToken(self) -> Token:
        # swith-case
        c = self.sr.readSkipWhitespace()
        if c == TokenType.OP_ASSIGN: # =, ==
            n = self.sr.top() # 查看下一个，不读出来
            if n == TokenType.OP_ASSIGN:
                return Token(TokenType.OP_EQ)
            else:
                return Token(TokenType.OP_ASSIGN)
        elif c == TokenType.OP_PLUS: # +
            return Token(TokenType.OP_PLUS)
        elif c == TokenType.OP_MINUS: # -
            return Token(TokenType.OP_MINUS)
        elif c == TokenType.OP_ASTERISK: # *
            return Token(TokenType.OP_ASTERISK)
        elif c == TokenType.OP_SLASH: # /
            return Token(TokenType.OP_SLASH)
        elif c == TokenType.OP_BANG: # !, !=
            n = self.sr.top()
            if n == TokenType.OP_ASSIGN:
                return Token(TokenType.OP_NEQ)
            else:
                return Token(TokenType.OP_BANG)
        elif c == TokenType.OP_LT: # <, <=
            n = self.sr.top()
            if n == TokenType.OP_ASSIGN:
                return Token(TokenType.OP_LTE)
            else:
                return Token(TokenType.OP_LT)
        elif c == TokenType.OP_GT: # >, >=
            n = self.sr.top()
            if n == TokenType.OP_ASSIGN:
                return Token(TokenType.OP_GTE)
            else:
                return Token(TokenType.OP_GT)
        elif c == TokenType.COMMA: # ,
            return Token(TokenType.COMMA)
        elif c == TokenType.SEMICOLON: # ;
            return Token(TokenType.SEMICOLON)
        elif c == TokenType.L_PAREN: # (
            return Token(TokenType.L_PAREN)
        elif c == TokenType.R_PAREN: # )
            return Token(TokenType.R_PAREN)
        elif c == TokenType.L_BRACE: # {
            return Token(TokenType.L_BRACE)
        elif c == TokenType.R_BRACE: # }
            return Token(TokenType.R_BRACE)
        elif c == tokenizer.EOF: # ,
            return Token(TokenType.EOF)
        else:
            if tokenizer.isLetter(c): # 处理单词
                word = self.sr.readWord(c)
                # 区分关键字和标识符
                keywordToken = KeywordMap.get(word)
                if keywordToken is None:
                    return Token(TokenType.IDENTIFIER, word)
                else:
                    return keywordToken
            elif tokenizer.isDigit(c): # 处理数字
                integer = self.sr.readInteger(c)
                return Token(TokenType.INTEGER, integer)
        
        return Token(TokenType.ILLEGAL)



if __name__ == "__main__":
    sr = SourceReader(io.BytesIO(b"ABC"))
    print(sr.read())
    print(sr.read())
    sr.unread("+")
    print(sr.read())
    print(sr.read())
    eof = sr.read()
    print(eof == tokenizer.EOF)

    print("====")

    sr = SourceReader(io.BytesIO(b"=+(){},;"))
    tz = Tokenizer(sr)
    while True:
        t = tz.nextToken()
        print(t)
        if t.tokenType == TokenType.EOF:
            break

    print("===")

    print(tokenizer.isDigit(tokenizer.EOF))
    print(tokenizer.isLetter(tokenizer.EOF))

    print("====")
    sr = SourceReader(io.BytesIO(b'''
        let five = 5;
        let ten = 10;

        let add = fn(x, y) {
        x + y;
        };

        let result = add(five, ten);
    '''))
    tz = Tokenizer(sr)
    tokens = []
    while True:
        t = tz.nextToken()
        tokens.append(t.__repr__())
        if t.tokenType == TokenType.EOF:
            break
    print(" ".join(tokens))

    print("====")
    sr = SourceReader(io.BytesIO(b'''
        let five = 5;
        let ten = 10;

        let add = fn(x, y) {
        x + y;
        };

        let result = add(five, ten);
        !-/*5;
        5 < 10 > 5;

        if (5 < 10) {
            return true;
        } else {
            return false;
        }
    '''))
    tz = Tokenizer(sr)
    tokens = []
    while True:
        t = tz.nextToken()
        tokens.append(t.__repr__())
        if t.tokenType == TokenType.EOF:
            break
    print(" ".join(tokens))

