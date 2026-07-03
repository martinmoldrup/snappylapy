from typing import overload, Union

class Base:
    @overload
    def do(self, x: int) -> int: ...
    
    @overload
    def do(self, x: str) -> str: ...
    
    def do(self, x: Union[int, str]) -> Union[int, str]:
        return x

class Extended(Base):
    @overload
    def do(self, x: float) -> float: ...
    
    @overload
    def do(self, x: int) -> int: ...
    
    @overload
    def do(self, x: str) -> str: ...
    
    def do(self, x: Union[int, str, float]) -> Union[int, str, float]:
        return x

if __name__ == "__main__":
    base = Base()
    extended = Extended()
    
    print(base.do(10))        # Output: 10
    print(base.do("hello"))   # Output: hello
    
    print(extended.do(10))     # Output: 10
    print(extended.do("world")) # Output: world
    print(extended.do(3.14))   # Output: 3.14