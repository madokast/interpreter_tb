'''
字节码
'''
from typing import List, Iterable, Iterator
from array import array

Byte = int

class Bytes:
    '''
    array[int] 高效数组，使用 array('B') 初始化为 8 为无符号数
    '''
    def __init__(self) -> None:
        self.proxy = array('B')
    def readInt(self, address:int, byteNumber:int) -> int:
        val = 0
        for i in range(byteNumber):
            val = val*256 + self.proxy[address+i]
        return val
    def pushInt(self, value:int, byteNumber:int) -> 'Bytes':
        temp = []
        for i in range(byteNumber):
            temp.append(value % 256)
            value //= 256
        self.proxy.extend(reversed(temp))
        return self
    def popInt(self, byteNumber:int) -> int:
        val = self.readInt(len(self) - byteNumber, byteNumber)
        self.proxy = self.proxy[:len(self) - byteNumber]
        return val
    def pushByte(self, byte:Byte) -> 'Bytes':
        self.proxy.append(byte)
        return self
    def extend(self, bytes:Iterable[int]) -> 'Bytes':
        self.proxy.extend(bytes)
        return self
    def __iter__(self)->Iterator[int]:
        return self.proxy.__iter__()
    def __len__(self) -> int:
        return len(self.proxy)
    def __getitem__(self, address:int) -> 'Byte':
        return self.proxy[address]
    def __str__(self) -> str:
        return str(list(self.proxy))

class ByteCode:
    def __init__(self) -> None:
        self.instrctions:Bytes = Bytes() # 二进制码
        self.constPool:Bytes = Bytes() # 常量池
    def __str__(self) -> str:
        ss:List[str] = []
        address = 0
        while address < len(self.instrctions):
            op = OprationCodes._INDEXES[self.instrctions[address]]
            ss.append(OprationCodes.string(address, self))
            address += op.length
        return str(self.instrctions)+"\n"+"\n".join(ss)


class OprationCode:
    '''
    字节码
    code 编码
    operandNumber 操作数数目
    mnemonic 助记符
    description 描述
    '''
    def __init__(self, code:Byte, operandNumber:int, mnemonic:str) -> None:
        self.code = code
        self.operandNumber = operandNumber
        self.length = operandNumber + 1
        self.mnemonic = mnemonic

class OprationCodes:
    NOOP = OprationCode(Byte(0), 0, "NOOP")
    LOADI = OprationCode(Byte(1), 2, "LOADI") # LOADI i j; 将常量池中第 (i<<8)+j 位置常量以四字节整形入栈
    ADDI = OprationCode(Byte(2), 0, "ADDI") # 弹出栈顶的两个四字节整形元素，相加再入栈
    SUBI = OprationCode(Byte(3), 0, "SUBI") # 弹出栈顶的两个四字节整形元素，相减再入栈。栈中后者减去前者
    MULI = OprationCode(Byte(4), 0, "MULI") # 弹出栈顶的两个四字节整形元素，相乘法再入栈
    DIVI = OprationCode(Byte(5), 0, "DIVI") # 弹出栈顶的两个四字节整形元素，相除法再入栈
    POPI = OprationCode(Byte(6), 0, "POPI") # 弹出栈顶的四字节整形元素
    PUSHBT = OprationCode(Byte(7), 0, "PUSHBT") # 将布尔值 TRUE （四字节整形 1）压入栈中
    PUSHBF = OprationCode(Byte(8), 0, "PUSHBF") # 将布尔值 FALSE（四字节整形 0）压入栈中
    EQI = OprationCode(Byte(9), 0, "EQI") # 弹出栈顶的两个四字节整形元素，判断相等，将结果以 1/0 入栈
    NEQI = OprationCode(Byte(10), 0, "NEQI") # 弹出栈顶的两个四字节整形元素，判断不相等，将结果以 1/0 入栈
    GTI = OprationCode(Byte(11), 0, "GTI") # 弹出栈顶的两个四字节整形元素，判断大于，将结果以 1/0 入栈
    GTEI = OprationCode(Byte(12), 0, "GTEI") # 弹出栈顶的两个四字节整形元素，判断大于等于，将结果以 1/0 入栈
    LTI = OprationCode(Byte(13), 0, "LTI") # 弹出栈顶的两个四字节整形元素，判断小于，将结果以 1/0 入栈
    LTEI = OprationCode(Byte(14), 0, "LTEI") # 弹出栈顶的两个四字节整形元素，判断小于等于，将结果以 1/0 入栈
    MINUSI = OprationCode(Byte(15), 0, "MINUSI") # 弹出栈顶的一个四字节整形元素，反转符号后入栈
    BANGB = OprationCode(Byte(16), 0, "BANGB") # 弹出栈顶的一个四字节整形元素，视为 0/1 布尔，反转后入栈

    _INDEXES:List[OprationCode] = [NOOP, LOADI, ADDI, SUBI, MULI, DIVI, POPI, PUSHBT, PUSHBF, EQI, NEQI, GTI, GTEI, LTI, LTEI, MINUSI, BANGB]
    @staticmethod
    def string(address:int, bytecode:ByteCode) -> str:
        if bytecode.instrctions[address] == OprationCodes.NOOP.code:
            return f"{OprationCodes.NOOP.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.LOADI.code:
            constIndex = bytecode.instrctions.readInt(address+1, OprationCodes.LOADI.operandNumber)
            return f"{OprationCodes.LOADI.mnemonic} #{constIndex}; {bytecode.constPool.readInt(constIndex, 4)}"
        if bytecode.instrctions[address] == OprationCodes.ADDI.code:
            return f"{OprationCodes.ADDI.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.SUBI.code:
            return f"{OprationCodes.SUBI.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.MULI.code:
            return f"{OprationCodes.MULI.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.DIVI.code:
            return f"{OprationCodes.DIVI.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.POPI.code:
            return f"{OprationCodes.POPI.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.PUSHBT.code:
            return f"{OprationCodes.PUSHBT.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.PUSHBF.code:
            return f"{OprationCodes.PUSHBF.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.EQI.code:
            return f"{OprationCodes.EQI.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.NEQI.code:
            return f"{OprationCodes.NEQI.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.GTI.code:
            return f"{OprationCodes.GTI.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.GTEI.code:
            return f"{OprationCodes.GTEI.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.LTI.code:
            return f"{OprationCodes.LTI.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.LTEI.code:
            return f"{OprationCodes.LTEI.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.MINUSI.code:
            return f"{OprationCodes.MINUSI.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.BANGB.code:
            return f"{OprationCodes.BANGB.mnemonic};"
        raise Exception(f"unknow operation code {bytecode.instrctions[address]}")

class Sizes:
    I = 4

if __name__ == "__main__":
    bytes = Bytes()
    bytes.pushByte(Byte(0))
    bytes.pushByte(Byte(0))
    bytes.pushByte(Byte(2))
    bytes.pushByte(Byte(22))
    print(bytes, bytes.readInt(0, 4))

    bytes = Bytes()
    bytes.pushInt(534, 2)
    print(bytes, bytes.readInt(0, 2))

    bytecode = ByteCode()
    bytecode.instrctions.pushByte(OprationCodes.LOADI.code)
    bytecode.instrctions.pushInt(0, 2)
    bytecode.constPool.pushInt(114514, 4)
    print(OprationCodes.string(0, bytecode))

    bytecode.instrctions.pushByte(OprationCodes.NOOP.code)
    print(bytecode)