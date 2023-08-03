'''
evaluator 解释器，解释 AST 树
'''

from it_ast import *
from it_object import *
from it_parser import parser
from typing import Dict, List
import io

class evaluator:
    @staticmethod
    def eval(input:io.IOBase) -> Object:
        program = parser.parse(input)
        e = Evaluator()
        e.eval(program)
        return e.result

class Enviroment:
    def __init__(self) -> None:
        self.stack:List[Dict[str, Object]] = [dict()]
    def currentStackFrame(self) -> Dict[str, Object]:
        if len(self.stack) == 0:
            raise Exception("stack empty")
        return self.stack[-1]
    def stackPush(self) -> None:
        self.stack.append(dict())
    def stackPop(self) -> None:
        if len(self.stack) == 0:
            raise Exception("stack empty")
        self.stack.pop()
    def put(self, name:str, object:Object) -> None:
        if name in self.currentStackFrame():
            raise Exception(f"redifined {name}")
        self.currentStackFrame()[name] = object
    def modify(self, name:str, object:Object) -> None:
        for frame in self.stack[::-1]: # 逆序
            if name in frame:
                frame[name] = object
                return
        raise Exception(f"undefined {name}")
    def get(self, name:str) -> Object:
        for frame in self.stack[::-1]: # 逆序
            if name in frame:
                return frame[name]
        raise Exception(f"undefined {name}")
    def __str__(self) -> str:
        return str(self.stack)

class Evaluator:
    BUILDIN_FUNC_PRINTIN = "println"
    def __init__(self) -> None:
        self.env = Enviroment()
        self.returnMode:bool = False
        self.result:Object = NullObject()
        self._init()
    def eval(self, node:Node) -> None:
        # switch node type
        nodeType = node.nodeType()
        # satatement
        if nodeType == NodeTypes.EMPTY_STATEMENT:
            self.result = NullObject()
        elif nodeType == NodeTypes.ASSIGN_STATEMENT: # assign
            assignSate = node.treatAs(AssignStatement)
            self.eval(assignSate.expression())
            self.env.modify(assignSate.identifier().name(), self.result)
        elif nodeType == NodeTypes.LET_STATEMENT: # let
            letState = node.treatAs(LetStatement)
            self.eval(letState.expression())
            self.env.put(letState.identifier().name(), self.result)
        elif nodeType == NodeTypes.RETURN_STATEMENT: # return
            self.eval(node.treatAs(ReturnStatement).expression())
            self.returnMode = True # 进入返回模式
        elif nodeType == NodeTypes.EXPRESSION_STATEMENT: # 表达式
            self.eval(node.treatAs(ExpressionStatement).expression())
        elif nodeType == NodeTypes.IF_STATEMENT:
            ifState = node.treatAs(IfStatement) # if
            self.eval(ifState.condition())
            if self.result.treatAs(BoolObject).value():
                self.eval(ifState.consequence())
            else:
                self.eval(ifState.alternative())
        elif nodeType == NodeTypes.WHILE_STATEMENT: # while
            whileState = node.treatAs(WhileStatement)
            while True:
                self.eval(whileState.condition())
                if not self.result.treatAs(BoolObject).value():
                    break
                self.eval(whileState.body())
                if self.returnMode: # 循环体需要检查 return 标识，否则空转
                    break
        elif nodeType == NodeTypes.BLOCK_STATEMENT: # 代码块，注意检查 return 标识，注意进入前后环境变更
            self.env.stackPush()
            for statement in node.treatAs(Block).statements():
                if self.returnMode:
                    break
                self.eval(statement)
            self.env.stackPop()
        # expression
        elif nodeType == NodeTypes.IDENTIFIER_EXPRESSION: # 标识符
            name = node.treatAs(IdentifierNode).name()
            self.result = self.env.get(name)
        elif nodeType == NodeTypes.INTEGER_LITERAL_EXPRESSION: # 整形字面量
            self.result = IntegerObject(node.treatAs(IntegerLiteral).integerValue())
        elif nodeType == NodeTypes.BOOL_LITERAL_EXPRESSION: # 布尔字面量
            self.result = BoolObject(node.treatAs(BoolLiteral).boolValue())
        elif nodeType == NodeTypes.FUNC_LITERAL_EXPRESSION: # 函数定义
            funcLit = node.treatAs(FuncLiteral)
            self.result = FuncObject(funcLit.parameterNames(), funcLit.body())
        elif nodeType == NodeTypes.PREFIX_EXPRESSION: # 前缀运算
            prefixExpr = node.treatAs(PrefixExpression)
            self.eval(prefixExpr.rawExpression())
            self.result = operation.unary(prefixExpr.prefixType(), self.result)
        elif nodeType == NodeTypes.BINARY_EXPRESSION: # 二元运算
            binaryExpr = node.treatAs(BinaryOperatorExpression)
            self.eval(binaryExpr.left())
            leftResult = self.result
            self.eval(binaryExpr.right())
            rightResult = self.result
            self.result = operation.binary(binaryExpr.operatorType(), leftResult, rightResult)
        elif nodeType == NodeTypes.FUNC_CALLER_EXPRESSION: # 函数调用
            callerExpr = node.treatAs(FuncCaller)
            self.eval(callerExpr.callee())
            funcObj = self.result.treatAs(FuncObject) # 对 callee 求职就拿到了 funcObj
            self.env.stackPush() # 进栈
            for i in range(len(funcObj.parameters())): # 准备实参
                self.eval(callerExpr.arguments()[i])
                self.env.put(funcObj.parameters()[i], self.result)
                # 对于内置函数 println 处理
                if isinstance(callerExpr.callee(), IdentifierNode) and callerExpr.callee().treatAs(IdentifierNode).name() == Evaluator.BUILDIN_FUNC_PRINTIN:
                    print(self.result)
            self.eval(funcObj.body()) # 计算函数体
            self.env.stackPop() # 退栈
            self.returnMode = False # 退出返回模式
        else:
            raise Exception(f"unknown node {node} type {nodeType}")
    def _init(self) -> None:
        # 加入内置函数 println(a)
        if True:
            self.env.put(Evaluator.BUILDIN_FUNC_PRINTIN, FuncObject(["obj"], Block()))

if __name__ == "__main__":
    def _eval(code:str) -> None:
        obj = evaluator.eval(io.BytesIO(code.encode("ascii")))
        print(f"{code}\n==>{obj}\n")

    _eval("123;")
    _eval("true;")
    _eval("false;")
    _eval("-123;")
    _eval("!true;")
    _eval("!false;")
    _eval("20+30;")
    _eval("20-30;")
    _eval("20*30;")
    _eval("50/20;")
    _eval("50>20;")
    _eval("50>100;")
    _eval("50>=20;")
    _eval("50>=50;")
    _eval("50>=100;")
    _eval("50<=100;")
    _eval("50<=50;")
    _eval("50<=40;")
    _eval("50==40;")
    _eval("50==50;")
    _eval("true==true;")
    _eval("false==true;")
    _eval("false!=true;")
    _eval("true!=true;")
    _eval("50!=50;")
    _eval("40!=50;")
    _eval("!false==true;")
    _eval("1+2+3+4==4+3+2+1;")
    _eval("if (5>2) {12;} else {21;}")
    _eval("if (1+1==3) {12;}")
    _eval("return 1+5;")
    _eval("if (2+3>5) {return 12;} else {return 21;}")
    _eval("return 1; return 2;")
    _eval("1; return 2;")
    _eval("1; return 2;3;")
    _eval("if (10>1) { if(10>1) {return 10;} return 1; }")
    _eval("let a = 123; let b = 312; a;")
    _eval("let a = 123; let b = 312; a + b;")
    _eval("let a = 5; let b = a; let c = a + b + 5; c;")
    _eval("let a = fn(a) {return a+1;}; a(11+11); a;")
    _eval("let add = fn(a,b,c,d) {return a+b+c+d;}; add(1,2,3,4);")
    _eval("let max = fn(x,y) {if(x>y){return x;}else{return y;}}; max(5, 10);")
    _eval("let fa = fn(n) {if(n==0){return 1;}else{return fa(n-1)*n;}}; fa(6);")
    _eval("fn(a, b) {return a*10+b;} (5,6);")
    _eval("let a = 5; fn(b) {return a*10+b;} (6);")
    _eval("let a = 5; let f5 = fn(b) {return a*10+b;}; let b = 7; let f7 = fn(d, f) {return b*100 + f(d);}; f7(6, f5);")
    _eval("while(true){return 123;}return 321;")
    _eval("let i = 0; while(true) {i=i+1; if (i==100){return i;}}")
    _eval("println(123);")