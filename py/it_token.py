from typing import Dict

class TokenType:
    '''
     词法单元 token 的类型，枚举类
    '''
    ILLEGAL = "ILLEGAL" # 非法类型
    EOF  = "EOF" # 结束标记
    # 标识符
    IDENTIFIER = "ID"
    INTEGER = "INT"
    # 运算符
    OP_ASSIGN = "="
    OP_PLUS = "+"
    OP_MINUS = "-"
    OP_ASTERISK = "*"
    OP_SLASH = "/"
    OP_BANG = "!"
    OP_EQ = "=="
    OP_NEQ = "!="
    OP_LT = "<"
    OP_LTE = "<="
    OP_GT = ">"
    OP_GTE = ">="

    # 分隔符
    COMMA = ","
    SEMICOLON = ";"
    # 括号
    L_PAREN = "("
    R_PAREN = ")"
    L_BRACE = "{"
    R_BRACE = "}"
    # 关键字
    KW_FUNC = "fn"
    KW_LET = "let"
    KW_IF = "if"
    KW_ELSE = "else"
    KW_RETURN = "return"
    KW_TRUE = "true"
    KW_FALSE = "false"

class Token:
    '''
    词法单元：词法类型 TokenType + 字面量 literal
    '''
    def __init__(self, tokenType:str, literal:str = "") -> None:
        self.tokenType = tokenType
        self.literal = literal
    def __str__(self) -> str:
        s = self.tokenType
        if len(self.literal) > 0:
            s += "(" + self.literal + ")"
        return s
    def __repr__(self) -> str:
        if len(self.literal) > 0:
            return self.literal
        else:
            return self.tokenType


KeywordMap:Dict[str, Token] = {
    TokenType.KW_FUNC:Token(TokenType.KW_FUNC),
    TokenType.KW_LET:Token(TokenType.KW_LET),
}

if __name__ == "__main__":
    tokens = [
        Token(TokenType.IDENTIFIER, "a"),
        Token(TokenType.OP_ASSIGN),
        Token(TokenType.INTEGER, "10"),
        Token(TokenType.OP_PLUS),
        Token(TokenType.INTEGER, "20"),
        Token(TokenType.SEMICOLON),
        Token(TokenType.EOF)
    ]
    for t in tokens:
        print(t)
    print(tokens)
