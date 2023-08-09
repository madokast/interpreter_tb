'''
编译器
'''
import it_interpreter.it_ast as ast # 各种表达式、语句
from it_compiler.it_code import Bytes, ByteCode, OprationCode, OprationCodes
from it_interpreter.it_token import TokenType, TokenTypes


class Compiler:
    def __init__(self) -> None:
        self.bytecode:ByteCode = ByteCode()
    def compile(self, node:ast.Node) -> None:
        nodeType = node.nodeType()
        if nodeType == ast.NodeTypes.PROGRAM_STATEMENT: # program
            for s in node.treatAs(ast.Program).statements():
                self.compile(s)
        elif nodeType == ast.NodeTypes.IF_STATEMENT: # if
            # if(a){b}else{c} 翻译为 a; JUMPF #1; b; JUMP #2; [#1] c; [#2] end; 
            ifState = node.treatAs(ast.IfStatement)
            self.compile(ifState.condition()) # 计算条件
            self._addInstraction(OprationCodes.JUMPF, Bytes().pushInt(-1, OprationCodes.JUMPF.operandNumber)) # JUMPF 先填充 -1，等知道跳转位置后回写
            jumpF = self.bytecode.instrctions.size() - OprationCodes.JUMPF.operandNumber # 记录 JUMPF 回写位置
            self.compile(ifState.consequence()) # consequence 
            self._addInstraction(OprationCodes.JUMP, Bytes().pushInt(-1, OprationCodes.JUMP.operandNumber))# JUMP 先填充 -1，
            jump = self.bytecode.instrctions.size() - OprationCodes.JUMP.operandNumber # 记录 JUMP 回写位置
            self.bytecode.instrctions.replace(jumpF, Bytes().pushInt(self.bytecode.instrctions.size(), OprationCodes.JUMPF.operandNumber)) # 回写 JUMPF
            self.compile(ifState.alternative())
            self.bytecode.instrctions.replace(jump, Bytes().pushInt(self.bytecode.instrctions.size(), OprationCodes.JUMP.operandNumber)) # 回写
        elif nodeType == ast.NodeTypes.BLOCK_STATEMENT: # block
            for s in node.treatAs(ast.Block).statements():
                self.compile(s)
        elif nodeType == ast.NodeTypes.EXPRESSION_STATEMENT: # expr_state 执行完后需要弹栈
            self.compile(node.treatAs(ast.ExpressionStatement).expression())
            self._addInstraction(OprationCodes.POPI, Bytes())
        elif nodeType == ast.NodeTypes.EMPTY_STATEMENT: # empty
            self._addInstraction(OprationCodes.NOOP, Bytes())
        elif nodeType == ast.NodeTypes.BINARY_EXPRESSION: # 二元
            biExpr = node.treatAs(ast.BinaryOperatorExpression)
            self.compile(biExpr.left())
            self.compile(biExpr.right())
            self._addBinaryOpeatorInstraction(biExpr.operatorType())
        elif nodeType == ast.NodeTypes.PREFIX_EXPRESSION: # 一元
            preExpr = node.treatAs(ast.PrefixExpression)
            self.compile(preExpr.rawExpression())
            if preExpr.prefixType() == TokenTypes.OP_MINUS:
                self._addInstraction(OprationCodes.MINUSI, Bytes())
            elif preExpr.prefixType() == TokenTypes.OP_BANG:
                self._addInstraction(OprationCodes.BANGB, Bytes())
            else:
                raise Exception(f"unknown prefix token type {preExpr.prefixType()}")
        elif nodeType == ast.NodeTypes.INTEGER_LITERAL_EXPRESSION: # int_literal_expr
            addr = self._addIntConstValue(node.treatAs(ast.IntegerLiteral).integerValue(), 4)
            self._addInstraction(OprationCodes.LOADI, Bytes().pushInt(addr, OprationCodes.LOADI.operandNumber))
        elif nodeType == ast.NodeTypes.BOOL_LITERAL_EXPRESSION: # bool_literal_expr
            self._addInstraction(OprationCodes.PUSHBT if node.treatAs(ast.BoolLiteral).boolValue() else OprationCodes.PUSHBF, Bytes())
        else:
            raise Exception(f"unknown node type {nodeType}")
    def _addInstraction(self, oprationCode:OprationCode, operands:Bytes) -> None:
        self.bytecode.instrctions.pushByte(oprationCode.code)
        self.bytecode.instrctions.extend(operands)
    def _addIntConstValue(self, value:int, byteNumber:int) -> int:
        addr = len(self.bytecode.constPool)
        self.bytecode.constPool.pushInt(value, byteNumber)
        return addr
    def _addBinaryOpeatorInstraction(self, tokenType:TokenType) -> None:
        if tokenType == TokenTypes.OP_PLUS:
            self._addInstraction(OprationCodes.ADDI, Bytes())
        elif tokenType == TokenTypes.OP_MINUS:
            self._addInstraction(OprationCodes.SUBI, Bytes())
        elif tokenType == TokenTypes.OP_ASTERISK:
            self._addInstraction(OprationCodes.MULI, Bytes())
        elif tokenType == TokenTypes.OP_SLASH:
            self._addInstraction(OprationCodes.DIVI, Bytes())
        elif tokenType == TokenTypes.OP_EQ:
            self._addInstraction(OprationCodes.EQI, Bytes())
        elif tokenType == TokenTypes.OP_NEQ:
            self._addInstraction(OprationCodes.NEQI, Bytes())
        elif tokenType == TokenTypes.OP_GT:
            self._addInstraction(OprationCodes.GTI, Bytes())
        elif tokenType == TokenTypes.OP_GTE:
            self._addInstraction(OprationCodes.GTEI, Bytes())
        elif tokenType == TokenTypes.OP_LT:
            self._addInstraction(OprationCodes.LTI, Bytes())
        elif tokenType == TokenTypes.OP_LTE:
            self._addInstraction(OprationCodes.LTEI, Bytes())
        else:
            raise Exception(f"unknown token type {tokenType}")

