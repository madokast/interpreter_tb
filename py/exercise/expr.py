'''
解析表达式的小练习
支持四则运算和括号
'''

from typing import List

# 优先级字典
PriorityDict = {')':0, '+':1, '-':1, '*':2, '/':2}

def parseExpr(tokens:List, currentPriority:int = 0)->str:
    # 首先解析左值
    expr = parseLeft(tokens)
    # 然后只要优先级大于 currentPriority，就组成二元运算
    while len(tokens)>0 and PriorityDict[tokens[0]]>currentPriority:
        operator = tokens.pop(0)
        right = parseExpr(tokens, PriorityDict[operator])
        expr = "(" + expr + " " + operator + " " + right + ")"
    return expr
 
def parseLeft(tokens:List)->str:
    first = tokens.pop(0)
    if first == '(':
        expr = parseExpr(tokens)
        assert tokens.pop(0) == ')'
        return expr
    else:
        assert isinstance(first, int), str(first)
        return str(first)

if __name__ == "__main__":
    print(parseExpr([1]))
    print(parseExpr([1, '+', 2]))
    print(parseExpr([1, '+', 2, '+', 3]))
    print(parseExpr([1, '+', 2, '*', 3]))
    print(parseExpr([1, '*', '(', 2, '+', 3, ')']))
    print(parseExpr(['(', 1, '+', 2, ')', '/', '(', 3, '-', 4, ')']))
    print(parseExpr(['(', 10, '+', 20, ')', '/', '(', 3, '*', '(', 40, '+', 50, ')', ')']))