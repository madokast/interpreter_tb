'''
二元运算符优先级
'''
from it_token import TokenType, TokenTypes


class Prority:
    '''
    优先级
    '''
    LOWEST = 0 # 最低优先级
    @staticmethod
    def of(tokenType:TokenType)->int:
        if tokenType == TokenTypes.R_PAREN:
            return Prority.LOWEST
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
