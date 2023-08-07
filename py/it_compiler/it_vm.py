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
        elif opCode == OprationCodes.POPI.code: # popi
            self.stack.popInt(Sizes.I)
            self.ip += OprationCodes.POPI.length
        elif opCode == OprationCodes.PUSHBT.code: # pushbt
            self.stack.pushInt(1, Sizes.I)
            self.ip += OprationCodes.PUSHBT.length
        elif opCode == OprationCodes.PUSHBF.code: # pushbf
            self.stack.pushInt(0, Sizes.I)
            self.ip += OprationCodes.PUSHBF.length
        elif opCode == OprationCodes.EQI.code: # eq
            right = self.stack.popInt(Sizes.I)
            left = self.stack.popInt(Sizes.I)
            self.stack.pushInt(1 if left == right else 0, Sizes.I)
            self.ip += OprationCodes.EQI.length
        elif opCode == OprationCodes.NEQI.code: # neq
            right = self.stack.popInt(Sizes.I)
            left = self.stack.popInt(Sizes.I)
            self.stack.pushInt(1 if left != right else 0, Sizes.I)
            self.ip += OprationCodes.NEQI.length
        elif opCode == OprationCodes.GTI.code: # gt
            right = self.stack.popInt(Sizes.I)
            left = self.stack.popInt(Sizes.I)
            self.stack.pushInt(1 if left > right else 0, Sizes.I)
            self.ip += OprationCodes.GTI.length
        elif opCode == OprationCodes.GTEI.code: # gte
            right = self.stack.popInt(Sizes.I)
            left = self.stack.popInt(Sizes.I)
            self.stack.pushInt(1 if left >= right else 0, Sizes.I)
            self.ip += OprationCodes.GTEI.length
        elif opCode == OprationCodes.LTI.code: # lt
            right = self.stack.popInt(Sizes.I)
            left = self.stack.popInt(Sizes.I)
            self.stack.pushInt(1 if left < right else 0, Sizes.I)
            self.ip += OprationCodes.LTI.length
        elif opCode == OprationCodes.LTEI.code: # lte
            right = self.stack.popInt(Sizes.I)
            left = self.stack.popInt(Sizes.I)
            self.stack.pushInt(1 if left <= right else 0, Sizes.I)
            self.ip += OprationCodes.LTEI.length
        elif opCode == OprationCodes.MINUSI.code: # minus
            val = self.stack.popInt(Sizes.I)
            self.stack.pushInt(-val, Sizes.I)
            self.ip += OprationCodes.MINUSI.length
        elif opCode == OprationCodes.BANGB.code: # bang
            val = self.stack.popInt(Sizes.I)
            if val != 0 and val != 1:
                raise Exception(f"BANGB cannot operate on {val}")
            self.stack.pushInt(1 - val, Sizes.I)
            self.ip += OprationCodes.BANGB.length
        else:
            raise Exception(f"unknown operation code {opCode}")
    def __str__(self) -> str:
        return f"[it_VM] ip:{self.ip}\nstack:{self.stack}"
