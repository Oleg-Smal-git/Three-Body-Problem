import config
import math


class Vector:
    def __init__(self, x=0.0, y=0.0):
        if (
                (isinstance(x, int) or isinstance(x, float)) and
                (isinstance(y, int) or isinstance(y, float))
        ):
            self.x = x
            self.y = y
        else:
            raise TypeError(f"Incompatible argument types: x: {type(x)}, y: {type(y)}")

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(
                x=self.x + other.x,
                y=self.y + other.y
            )
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(
                x=self.x - other.x,
                y=self.y - other.y
            )
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(
                x=self.x * other,
                y=self.y * other
            )
        elif isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector(
                x=self.x / other,
                y=self.y / other
            )

    def __copy__(self):
        new = type(self)()
        new.__dict__.update(self.__dict__)
        return new

    def __iadd__(self, other):
        if isinstance(other, Vector):
            self.x += other.x
            self.y += other.y
            return self
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def __isub__(self, other):
        if isinstance(other, Vector):
            self.x -= other.x
            self.y -= other.y
            return self
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def __imul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
            return self
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def __idiv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x /= other
            self.y /= other
            return self
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def length(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))


class Body:
    def __init__(self, mass=0.0, position=Vector(), velocity=Vector(), acceleration=Vector()):
        if (
            (isinstance(mass, int) or isinstance(mass, float)) and
            isinstance(position, Vector) and
            isinstance(velocity, Vector) and
            isinstance(acceleration, Vector)
        ):
            self.mass = mass
            self.position = position
            self.velocity = velocity
            self.acceleration = acceleration
        else:
            raise TypeError(
                f"Incompatible argument types: " +
                f"mass: {type(mass)}, position: {type(position)}, " +
                f"velocity: {type(velocity)}, acceleration: {type(acceleration)}"
            )

    def attraction(self, other):
        if isinstance(other, Body):
            self_to_other = Vector(
                x=other.position.x - self.position.x,
                y=other.position.y - self.position.y
            )
            try:
                return self_to_other * config.CONSTANTS["gravitational_constant"] *\
                   other.mass / math.pow(self_to_other.length(), 3)
            except ZeroDivisionError:
                return self.acceleration
        else:
            raise TypeError(f"Incompatible second argument type: {type(other)}")

    def step(self, delta_time=0.0, others=None):
        if others is None:
            others = []
        if (
            (isinstance(delta_time, int) or isinstance(delta_time, float)) and
            isinstance(others, list)
        ):
            self.acceleration = sum(
                [self.attraction(body) for body in others],
                start=Vector()
            )
            self.velocity += self.acceleration * delta_time
            self.position += self.velocity * delta_time + self.acceleration * math.pow(delta_time, 2) / 2
        else:
            raise TypeError(f"Incompatible second argument type: {type(delta_time)}")
