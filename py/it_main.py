import sys
import io
import it_tokenizer
import it_parser
import it_evaluator
import it_ast
import time

def REPL()->None:
    evaluator = it_evaluator.Evaluator()
    while True:
        print("it >> ", end="")
        code = ""
        try:
            code = input()
        except:
            return
        if code == ":q":
            return
        tokens = it_tokenizer.tokenizer.tokenize(io.BytesIO(code.encode("ascii")))
        print("\n".join((str(t) for t in tokens)))
        ast = it_ast.EmptyStatement()
        try:
            ast = it_parser.parser.parse(io.BytesIO(code.encode("ascii")))
            print("AST::", ast)
        except Exception as e:
            print("parse error", e)
            continue
        evaluator.eval(ast)
        print(evaluator.result, evaluator.env)
        if evaluator.returnMode:
            break

def run(code:io.IOBase)->None:
    start = time.time()
    ast = it_parser.parser.parse(code)
    it_evaluator.Evaluator().eval(ast)
    print("runtime" ,time.time() - start)


def help()->None:
    print("interpreter_tb https://github.com/madokast/interpreter_tb")
    print("/         REPL")
    print("-h        help")
    print("-f [file] execute file")
    print("-c [code] execute code")


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 1:
        REPL()
    elif len(argv) == 3:
        if (argv[1] == '-f'):
            with open(argv[2], encoding="utf-8") as f:
                run(io.BytesIO(f.read().encode("ascii")))
        elif (argv[1] == '-c'):
            run(io.BytesIO(argv[2].encode("ascii")))
        else:
            help()
    else:
        help()


