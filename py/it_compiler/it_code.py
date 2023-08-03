'''
字节码
'''
from typing import List

class Byte:
    '''
    即 uint8 无符号 8 位整数
    '''
    def __init__(self, value:int) -> None:
        if value < 0 or value > 255:
            raise Exception(F"byte overflow {value}")
        self.value = value
    def __eq__(self, that: object) -> bool:
        if isinstance(that, Byte):
            return that.value == self.value
        return False
    def __str__(self) -> str:
        return str(self.value)
    def __repr__(self) -> str:
        return str(self)

class Bytes(List[Byte]):
    def readInt(self, address:int, byteNumber:int) -> int:
        val = 0
        for i in range(byteNumber):
            val = val*256 + self[address+i].value
        return val
    def pushInt(self, value:int, byteNumber:int) -> 'Bytes':
        temp = []
        for i in range(byteNumber):
            temp.append(Byte(value % 256))
            value //= 256
        self.extend(reversed(temp))
        return self
    def pushByte(self, byte:Byte) -> 'Bytes':
        self.append(byte)
        return self

class ByteCode:
    def __init__(self) -> None:
        self.instrctions:Bytes = Bytes() # 二进制码
        self.constPool:Bytes = Bytes() # 常量池
    def __str__(self) -> str:
        ss:List[str] = []
        address = 0
        while address < len(self.instrctions):
            op = OprationCodes._INDEXES[self.instrctions[address].value]
            ss.append(OprationCodes.string(address, self))
            address += op.length
        return "\n".join(ss)


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
    LOADI = OprationCode(Byte(1), 2, "LOADI") # LOADI i j; 将常量值中第 (i<<8)+j 位置常量以四字节整形入栈

    _INDEXES:List[OprationCode] = [NOOP, LOADI]
    @staticmethod
    def string(address:int, bytecode:ByteCode) -> str:
        if bytecode.instrctions[address] == OprationCodes.NOOP.code:
            return f"{OprationCodes.NOOP.mnemonic};"
        if bytecode.instrctions[address] == OprationCodes.LOADI.code:
            constIndex = bytecode.instrctions.readInt(address+1, OprationCodes.LOADI.operandNumber)
            return f"{OprationCodes.LOADI.mnemonic} #{constIndex}({bytecode.constPool.readInt(constIndex, 4)});"
        raise Exception(f"unknow operation code {bytecode.instrctions[address]}")

if __name__ == "__main__":
    bytes = Bytes()
    bytes.append(Byte(0))
    bytes.append(Byte(0))
    bytes.append(Byte(2))
    bytes.append(Byte(22))
    print(bytes, bytes.readInt(0, 4))

    bytes = Bytes()
    bytes.pushInt(534, 2)
    print(bytes, bytes.readInt(0, 2))

    bytecode = ByteCode()
    bytecode.instrctions.pushByte(OprationCodes.LOADI.code)
    bytecode.instrctions.pushInt(0, 2)
    bytecode.constPool.pushInt(114514, 4)
    print(OprationCodes.string(0, bytecode))

    bytecode.instrctions.append(OprationCodes.NOOP.code)
    print(bytecode)