'''
二元运算符优先级
'''
from it_token import TokenType, TokenTypes


class Priority:
    '''
    优先级
    '''
    LOWEST = 0 # 最低优先级
    @staticmethod
    def of(tokenType:TokenType)->int:
        if tokenType == TokenTypes.R_PAREN: # 解析 (1) 就会遇到右括号 )
            return Priority.LOWEST
        elif tokenType == TokenTypes.SEMICOLON: # return expr; 后面会遇到 ;
            return Priority.LOWEST
        elif tokenType == TokenTypes.L_BRACE: # if expr {} 后面会遇到 {
            return Priority.LOWEST
        elif tokenType == TokenTypes.COMMA: # 解析 add(1, 2) 中会遇到逗号 , {
            return Priority.LOWEST
        elif tokenType == TokenTypes.OP_EQ:
            return 1
        elif tokenType == TokenTypes.OP_LT:
            return 2
        elif tokenType == TokenTypes.OP_LTE:
            return 2
        elif tokenType == TokenTypes.OP_GT:
            return 2
        elif tokenType == TokenTypes.OP_GTE:
            return 2
        elif tokenType == TokenTypes.OP_PLUS:
            return 3
        elif tokenType == TokenTypes.OP_MINUS:
            return 3
        elif tokenType == TokenTypes.OP_ASTERISK:
            return 4
        elif tokenType == TokenTypes.OP_SLASH:
            return 4
        raise Exception(f"unexcept token type {tokenType}")
