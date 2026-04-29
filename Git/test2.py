name = 'Bob'
age = 20

print(name, age)
print('Hello, my name is: ', name)

number: int = 10
decimal: float = 2.5
text: str = 'Hello, world!'
active: bool = False

names: list = ['Bob', 'Anna', 'Luigi']
coordinates: tuple = (1.5, 2.5) # immutable, can't add or remove elements
unique: set = {1, 4, 2, 9} # can't have duplicates, unique values only
data: dict = {'name': 'Bob', 'age': 20}

name: str = 'Bob' # Type annotation for string
age: int = 'Eleven' # Error: string instead of integer

from typing import Final

VERSION: Final[str] = '1.0.12'
PI: Final[float] = 3.14159

from datetime import datetime

def show_date() -> None:
    print('This is the current date and time:')
    print(datetime.now())

show_date()

def greet(name: str) -> None:
    print(f'Hello, {name}!')

greet('Bob')
greet('Luigi')

def add(a: float, b: float) -> float:
    return a + b

print(add(1,2))

class Car:
    def __init__(self, brand: str, horsepower: int) -> None:
        self.brand = brand
        self.horsepower = horsepower

    def __str__(self) -> str:
        return f'{self.brand}, {self.horsepower}hp'
    
    def __add__(self, other) -> str:
        return f'{self.brand} & {other.brand}'
        
volvo: Car = Car('Volvo', 200)
bmw: Car = Car('BMW', 240)
print(volvo + bmw)
