
import sys
sys.path.append(r"D:\learn\repo\cpp\interpreter_tb\py")

import io
from it_interpreter import it_parser
from it_compiler import it_compiler

def _test(code:str)->None:
    AST = it_parser.parser.parse(io.BytesIO(code.encode("ascii")))
    c = it_compiler.Compiler()
    c.compile(AST)
    print(code, c.bytecode, '', sep='\n')

_test(";")
_test(";23;;;")
sys.exit(1)