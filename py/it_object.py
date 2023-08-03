'''
语言的对象系统，仅在 AST 解释器中使用
IntegerObject 整形对象
BoolObject 布尔对象
NullObject 空对象，出现在非表达式求值时
'''

from it_token import TokenTypes, TokenType
from it_ast import Block
from typing import Any, TypeVar, Type, List

class ObjectType(str):
    '''
    对象类型
    '''
    pass

class ObjectTypes:
    INTEGRE = ObjectType("INTEGRE")
    BOOL = ObjectType("BOOL")
    FUNC = ObjectType("FUNC")
    NULL = ObjectType("NULL")

class Object:
    T = TypeVar("T")
    def objectType(self):
        raise NotImplementedError
    def __str__(self) -> str:
        raise NotImplementedError
    def __repr__(self) -> str:
        return str(self)
    def treatAs(self, hint:Type[T]) -> T:
        if isinstance(self, hint):
            return self
        else:
            raise Exception(f"{self} if not {hint.__name__}")

class IntegerObject(Object):
    def __init__(self, value:int) -> None:
        super().__init__()
        self._value = value
    def objectType(self)->ObjectType:
        return ObjectTypes.INTEGRE
    def value(self)->int:
        return self._value
    def __str__(self) -> str:
        return str(self._value)
    
class BoolObject(Object):
    def __init__(self, value:bool) -> None:
        super().__init__()
        self._value = value
    def objectType(self)->ObjectType:
        return ObjectTypes.BOOL
    def value(self)->bool:
        return self._value
    def __str__(self) -> str:
        return "true" if self._value else "false"

class FuncObject(Object):
    def __init__(self, parameters:List[str], body:Block) -> None:
        super().__init__()
        self._parameters = parameters
        self._body = body
    def objectType(self)->ObjectType:
        return ObjectTypes.FUNC
    def parameters(self) -> List[str]:
        return self._parameters
    def body(self) -> Block:
        return self._body
    def __str__(self) -> str:
        return "func"

class NullObject(Object):
    def __init__(self) -> None:
        super().__init__()
    def objectType(self)->ObjectType:
        return ObjectTypes.NULL
    def __str__(self) -> str:
        return "null"
    
class operation:
    @staticmethod
    def unary(operator:TokenType, object:Object) -> Object:
        if object.objectType() == ObjectTypes.NULL:
            raise Exception(f"operate {operator} on null value")
        if operator == TokenTypes.OP_MINUS and object.objectType() == ObjectTypes.INTEGRE: # 负号
            return IntegerObject(-object.treatAs(IntegerObject).value())
        if operator == TokenTypes.OP_BANG and object.objectType() == ObjectTypes.BOOL: # 否定
            return BoolObject(not object.treatAs(BoolObject).value())
        raise Exception(f"invalid operation {operator} on {object}")
    @staticmethod
    def binary(operator:TokenType, left:Object, right:Object) -> Object: # 四则运算，大于小于等于不等于
        if left.objectType() == ObjectTypes.NULL or right.objectType() == ObjectTypes.NULL:
            raise Exception(f"operate {operator} on null value")
        if operator == TokenTypes.OP_PLUS and left.objectType() == ObjectTypes.INTEGRE and right.objectType() == ObjectTypes.INTEGRE: # +
            return IntegerObject(left.treatAs(IntegerObject).value() + right.treatAs(IntegerObject).value())
        if operator == TokenTypes.OP_MINUS and left.objectType() == ObjectTypes.INTEGRE and right.objectType() == ObjectTypes.INTEGRE: # -
            return IntegerObject(left.treatAs(IntegerObject).value() - right.treatAs(IntegerObject).value())
        if operator == TokenTypes.OP_ASTERISK and left.objectType() == ObjectTypes.INTEGRE and right.objectType() == ObjectTypes.INTEGRE: # *
            return IntegerObject(left.treatAs(IntegerObject).value() * right.treatAs(IntegerObject).value())
        if operator == TokenTypes.OP_SLASH and left.objectType() == ObjectTypes.INTEGRE and right.objectType() == ObjectTypes.INTEGRE: # /
            return IntegerObject(left.treatAs(IntegerObject).value() // right.treatAs(IntegerObject).value())
        
        if operator == TokenTypes.OP_GT and left.objectType() == ObjectTypes.INTEGRE and right.objectType() == ObjectTypes.INTEGRE: # >
            return BoolObject(left.treatAs(IntegerObject).value() > right.treatAs(IntegerObject).value())
        if operator == TokenTypes.OP_GTE and left.objectType() == ObjectTypes.INTEGRE and right.objectType() == ObjectTypes.INTEGRE: # >=
            return BoolObject(left.treatAs(IntegerObject).value() >= right.treatAs(IntegerObject).value())
        if operator == TokenTypes.OP_LT and left.objectType() == ObjectTypes.INTEGRE and right.objectType() == ObjectTypes.INTEGRE: # <
            return BoolObject(left.treatAs(IntegerObject).value() < right.treatAs(IntegerObject).value())
        if operator == TokenTypes.OP_LTE and left.objectType() == ObjectTypes.INTEGRE and right.objectType() == ObjectTypes.INTEGRE: # <=
            return BoolObject(left.treatAs(IntegerObject).value() <= right.treatAs(IntegerObject).value())
        
        if operator == TokenTypes.OP_EQ and left.objectType() == ObjectTypes.INTEGRE and right.objectType() == ObjectTypes.INTEGRE: # == int
            return BoolObject(left.treatAs(IntegerObject).value() == right.treatAs(IntegerObject).value())
        if operator == TokenTypes.OP_EQ and left.objectType() == ObjectTypes.BOOL and right.objectType() == ObjectTypes.BOOL: # == bool
            return BoolObject(left.treatAs(BoolObject).value() == right.treatAs(BoolObject).value())

        if operator == TokenTypes.OP_NEQ and left.objectType() == ObjectTypes.INTEGRE and right.objectType() == ObjectTypes.INTEGRE: # != int
            return BoolObject(left.treatAs(IntegerObject).value() != right.treatAs(IntegerObject).value())
        if operator == TokenTypes.OP_NEQ and left.objectType() == ObjectTypes.BOOL and right.objectType() == ObjectTypes.BOOL: # != bool
            return BoolObject(left.treatAs(BoolObject).value() != right.treatAs(BoolObject).value())
        raise Exception(f"invalid operation {left} {operator} {right}")