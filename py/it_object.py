'''
语言的对象系统
IntegerObject 整形对象
BoolObject 布尔对象
NullObject 空对象，出现在非表达式求值时
'''

class ObjectType(str):
    '''
    对象类型
    '''
    pass

class ObjectTypes:
    INTEGRE = ObjectType("INTEGRE")
    BOOL = ObjectType("BOOL")
    NULL = ObjectType("NULL")

class Object:
    def objectType(self):
        raise NotImplementedError
    def __str__(self) -> str:
        raise NotImplementedError

class IntegerObject(Object):
    def __init__(self, value:int) -> None:
        super().__init__()
        self._value = value
    def objectType(self)->ObjectType:
        return ObjectTypes.INTEGRE
    def __str__(self) -> str:
        return str(self._value)
    
class BoolObject(Object):
    def __init__(self, value:bool) -> None:
        super().__init__()
        self._value = value
    def objectType(self)->ObjectType:
        return ObjectTypes.BOOL
    def __str__(self) -> str:
        return "true" if self._value else "false"

class NullObject(Object):
    def __init__(self) -> None:
        super().__init__()
    def objectType(self)->ObjectType:
        return ObjectTypes.NULL
    def __str__(self) -> str:
        return "null"