import sys
import io
import it_tokenizer

def REPL()->None:
    while True:
        print("it >> ", end="")
        s = ""
        try:
            s = input()
        except:
            return
        if s == "exit":
            return
        ts = it_tokenizer.tokenizer.tokenize(io.BytesIO(s.encode("ascii")))
        print("\n".join((str(t) for t in ts)))
        print(" ".join((t.__repr__() for t in ts)))

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 1:
        REPL()
    elif len(argv) == 2:
        if argv[1] == '-h':
            print("interpreter_tb https://github.com/madokast/interpreter_tb")
        else:
            with open(argv[1]) as f:
                print(f.read()) # TODO

