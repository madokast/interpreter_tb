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
    elif len(argv) == 2:
        help()
    elif len(argv) == 3:
        if (argv[1] == '-f'):
            with open(argv[2], encoding="utf-8") as f:
                print(f.read())
        elif (argv[1] == '-c'):
            code = argv[2]
            start = time.time()
            tokens = it_tokenizer.tokenizer.tokenize(io.BytesIO(code.encode("ascii")))
            ast = it_parser.parser.parse(io.BytesIO(code.encode("ascii")))
            evaluator = it_evaluator.Evaluator()
            evaluator.eval(ast)
            print(evaluator.result, time.time() - start)


