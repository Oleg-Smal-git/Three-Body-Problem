from constants import CONSTANTS
import math


class Vector:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        self.x = other.x
        self.y = other.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(other * self.x, other * self.y)

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __str__(self):
        return f"({self.x}, {self.y})"

    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


def name_generator():
    i = -1
    while True:
        i += 1
        yield f"body{i}"


name_gen = name_generator()


class Body:
    def __init__(self, position=Vector(), velocity=Vector(), acceleration=Vector(), mass=0.0):
        self.name = next(name_gen)
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass

    def calculate_attraction(self, other):
        multiplier = (CONSTANTS["gravity"] * other.mass) / ((other.position - self.position).length() ** 3)
        if (other.position - self.position).length() < 10:
            print(f"{other.name} -> {self.name} = {(other.position - self.position).length()}")
        return Vector(
            other.position.x - self.position.x,
            other.position.y - self.position.y
        ) * multiplier

    def calculate_total_acceleration(self, others):
        return sum(
            [self.calculate_attraction(body) for body in others],
            start=Vector()
        )

    def step(self, others):
        self.acceleration = self.calculate_total_acceleration(others)
        if self.velocity is None:
            self.velocity = Vector()
        self.velocity += self.acceleration * CONSTANTS["period"]
        self.position += self.velocity * CONSTANTS["period"] + (self.acceleration * CONSTANTS["period"] ** 2) / 2
        return self.position

