'''
编译器
'''
import it_interpreter.it_ast as ast # 各种表达式、语句
from it_compiler.it_code import Bytes, ByteCode, OprationCode, OprationCodes
from typing import List


class Compiler:
    def __init__(self) -> None:
        self.bytecode:ByteCode = ByteCode()
    def compile(self, node:ast.Node) -> None:
        nodeType = node.nodeType()
        if nodeType == ast.NodeTypes.PROGRAM_STATEMENT:
            for s in node.treatAs(ast.Program).statements():
                self.compile(s)
        elif nodeType == ast.NodeTypes.BLOCK_STATEMENT:
            for s in node.treatAs(ast.Block).statements():
                self.compile(s)
        elif nodeType == ast.NodeTypes.EXPRESSION_STATEMENT:
            self.compile(node.treatAs(ast.ExpressionStatement).expression())
        elif nodeType == ast.NodeTypes.EMPTY_STATEMENT:
            self._addInstraction(OprationCodes.NOOP, Bytes())
        elif nodeType == ast.NodeTypes.INTEGER_LITERAL_EXPRESSION:
            addr = self._addIntConstValue(node.treatAs(ast.IntegerLiteral).integerValue(), 4)
            self._addInstraction(OprationCodes.LOADI, Bytes().pushInt(addr, OprationCodes.LOADI.operandNumber))
        else:
            raise Exception(f"unknown node type {nodeType}")
    def _addInstraction(self, oprationCode:OprationCode, operands:Bytes) -> None:
        self.bytecode.instrctions.pushByte(oprationCode.code)
        self.bytecode.instrctions.extend(operands)
    def _addIntConstValue(self, value:int, byteNumber:int) -> int:
        addr = len(self.bytecode.constPool)
        self.bytecode.constPool.pushInt(value, byteNumber)
        return addr
    

if __name__ == "__main__":
    from it_interpreter import it_parser
    import io
    def _test(code:str)->None:
        AST = it_parser.parser.parse(io.BytesIO(code.encode("ascii")))
        c = Compiler()
        c.compile(AST)
        print(code, '\n', c.bytecode, '\n')

    _test(";")
