from it_compiler.it_code import Bytes, ByteCode, OprationCodes, Sizes

class VM:
    def __init__(self, bytecode:ByteCode) -> None:
        self.bytecode = bytecode
        self.stack:Bytes = Bytes()
        self.ip:int = 0 # 程序计数器
    def hasNext(self) -> bool:
        return self.ip < len(self.bytecode.instrctions)
    def step(self) -> None:
        opCode = self.bytecode.instrctions[self.ip]
        if opCode == OprationCodes.NOOP.code: # noop
            self.ip += OprationCodes.NOOP.length
        elif opCode == OprationCodes.LOADI.code: # loadi
            constIndex = self.bytecode.instrctions.readInt(self.ip+1, OprationCodes.LOADI.operandNumber)
            constValue = self.bytecode.constPool.readInt(constIndex, Sizes.I)
            self.stack.pushInt(constValue, Sizes.I)
            self.ip += OprationCodes.LOADI.length
        elif opCode == OprationCodes.ADDI.code: # addi
            right = self.stack.popInt(Sizes.I)
            left = self.stack.popInt(Sizes.I)
            self.stack.pushInt(left + right, Sizes.I)
            self.ip += OprationCodes.ADDI.length
        elif opCode == OprationCodes.SUBI.code: # subi
            right = self.stack.popInt(Sizes.I)
            left = self.stack.popInt(Sizes.I)
            self.stack.pushInt(left - right, Sizes.I)
            self.ip += OprationCodes.SUBI.length
        elif opCode == OprationCodes.MULI.code: # muli
            right = self.stack.popInt(Sizes.I)
            left = self.stack.popInt(Sizes.I)
            self.stack.pushInt(left * right, Sizes.I)
            self.ip += OprationCodes.MULI.length
        elif opCode == OprationCodes.DIVI.code: # divi
            right = self.stack.popInt(Sizes.I)
            left = self.stack.popInt(Sizes.I)
            self.stack.pushInt(left // right, Sizes.I)
            self.ip += OprationCodes.DIVI.length
        elif opCode == OprationCodes.POPI.code:
            self.stack.popInt(Sizes.I)
            self.ip += OprationCodes.POPI.length
        else:
            raise Exception(f"unknown operation code {opCode}")
    def __str__(self) -> str:
        return f"[it_VM] ip:{self.ip}\nstack:{self.stack}"
