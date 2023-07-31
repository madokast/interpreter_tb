'''
evaluator 解释器，解释 AST 树
'''

from it_ast import *
from it_object import *
from it_tokenizer import SourceReader, Tokenizer
from it_parser import parser
import io

class evaluator:
    @staticmethod
    def eval(input:io.IOBase) -> Object:
        program = parser.parse(input)
        return Evaluator().eval(program)

class Evaluator:
    def __init__(self) -> None:
        pass
    def eval(self, node:Node) -> Object:
        result:Object = NullObject()
        # switch node type
        nodeType = node.nodeType()
        if nodeType == NodeTypes.BLOCK_STATEMENT:
            for s in node.treatAs(Block).statements():
                result = self.eval(s)
        elif nodeType == NodeTypes.EXPRESSION_STATEMENT:
            return self.eval(node.treatAs(ExpressionStatement).expression())
        elif nodeType == NodeTypes.INTEGER_LITERAL_EXPRESSION:
            result = IntegerObject(node.treatAs(IntegerLiteral).integerValue())
        elif nodeType == NodeTypes.BOOL_LITERAL_EXPRESSION:
            result = BoolObject(node.treatAs(BoolLiteral).boolValue())
        else:
            raise Exception(f"unknown node {node} type {nodeType}")
        return result
            

if __name__ == "__main__":
    def _eval(code:str) -> None:
        obj = evaluator.eval(io.BytesIO(code.encode("ascii")))
        print(f"{code}\n==>{obj}\n")

    _eval("123;")
    _eval("true;")
    _eval("false;")