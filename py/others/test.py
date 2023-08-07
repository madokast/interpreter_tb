
import sys
import os
print(sys.path)
sys.path.append(os.path.dirname(sys.path[0]))

import io
from it_interpreter import it_parser
from it_compiler import it_compiler
from it_compiler.it_code import *
from it_compiler.it_vm import *

if __name__ == "__main__":
    bytecode = ByteCode()
    bytecode.instrctions.pushByte(OprationCodes.LOADI.code)
    bytecode.instrctions.pushInt(14, OprationCodes.LOADI.operandNumber)
    bytecode.constPool.extend([0]*14).pushInt(513, Sizes.I)
    vm = VM(bytecode)
    while vm.hasNext():
        vm.step()
    print(vm)

if __name__ == "__main__":
    def _test(code:str)->None:
        AST = it_parser.parser.parse(io.BytesIO(code.encode("ascii")))
        c = it_compiler.Compiler()
        c.compile(AST)
        print(">> " + code, "\n", c.bytecode, sep='')
        vm = VM(c.bytecode)
        while vm.hasNext():
            vm.step()
            print(vm, '\n')

    _test(";")
    _test(";23;;46;")
    _test("1+2;")
    _test("20/(10-6);")
    _test("true;")
    _test("false;")
    _test("2>4;")
    _test("-3;")
    _test("!(2<=4);")
    _test("!true;")