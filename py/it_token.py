from typing import Dict

class TokenType(str):
    pass

class TokenTypes:
    '''
    词法单元 token 的类型，枚举类
    '''
    ILLEGAL = TokenType("ILLEGAL") # 非法类型
    EOF  = TokenType("EOF") # 结束标记
    # 标识符
    IDENTIFIER = TokenType("ID")
    INTEGER = TokenType("INT")
    # 运算符
    OP_ASSIGN = TokenType("=")
    OP_PLUS = TokenType("+")
    OP_MINUS = TokenType("-")
    OP_ASTERISK = TokenType("*")
    OP_SLASH = TokenType("/")
    OP_BANG = TokenType("!")
    OP_EQ = TokenType("==")
    OP_NEQ = TokenType("!=")
    OP_LT = TokenType("<")
    OP_LTE = TokenType("<=")
    OP_GT = TokenType(">")
    OP_GTE = TokenType(">=")
    # 分隔符
    COMMA = TokenType(",")
    SEMICOLON = TokenType(";")
    # 括号
    L_PAREN = TokenType("(")
    R_PAREN = TokenType(")")
    L_BRACE = TokenType("{")
    R_BRACE = TokenType("}")
    # 关键字
    KW_FUNC = TokenType("fn")
    KW_LET = TokenType("let")
    KW_IF = TokenType("if")
    KW_ELSE = TokenType("else")
    KW_RETURN = TokenType("return")
    KW_TRUE = TokenType("true")
    KW_FALSE = TokenType("false")

class Token:
    '''
    词法单元：词法类型 TokenType + 字面量 literal
    '''
    def __init__(self, tokenType:TokenType, literal:str = "") -> None:
        self.tokenType = tokenType
        self.literal = literal
    def checkTokenType(self, tokenType:TokenType)->'Token':
        if self.tokenType != tokenType:
            raise Exception(f"type of token {self} is not {tokenType}")
        return self
    def __str__(self) -> str:
        s = self.tokenType
        if len(self.literal) > 0:
            s += "(" + self.literal + ")"
        return s
    def __repr__(self) -> str:
        if len(self.literal) > 0:
            return '`' + self.literal + '`'
        else:
            return self.tokenType


KeywordMap:Dict[str, Token] = {
    TokenTypes.KW_FUNC:Token(TokenTypes.KW_FUNC),
    TokenTypes.KW_LET:Token(TokenTypes.KW_LET),
    TokenTypes.KW_IF:Token(TokenTypes.KW_IF),
    TokenTypes.KW_ELSE:Token(TokenTypes.KW_ELSE),
    TokenTypes.KW_RETURN:Token(TokenTypes.KW_RETURN),
    TokenTypes.KW_TRUE:Token(TokenTypes.KW_TRUE),
    TokenTypes.KW_FALSE:Token(TokenTypes.KW_FALSE),
}

if __name__ == "__main__":
    tokens = [
        Token(TokenTypes.IDENTIFIER, "a"),
        Token(TokenTypes.OP_ASSIGN),
        Token(TokenTypes.INTEGER, "10"),
        Token(TokenTypes.OP_PLUS),
        Token(TokenTypes.INTEGER, "20"),
        Token(TokenTypes.SEMICOLON),
        Token(TokenTypes.EOF)
    ]
    for t in tokens:
        print(t)
    print(tokens)
