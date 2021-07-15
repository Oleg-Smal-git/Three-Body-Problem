from constants import CONSTANTS


class Vector:
    def __init__(self, x=None, y=None):
        self.x = x if x else 0
        self.y = y if y else 0

    def __eq__(self, other):
        self.x = other.x
        self.y = other.y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(other * self.x, other * self.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __imul__(self, other):
        self.x *= other
        self.y *= other

    def __len__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


class Body:
    def __init__(self, position=None, velocity=None, acceleration=None, mass=None):
        self.position = position if position else Vector()
        self.velocity = velocity if velocity else Vector()
        self.acceleration = acceleration if acceleration else Vector()
        self.mass = mass if mass else 0

    def calculate_attraction(self, other):
        return (CONSTANTS["gravity"] * other.mass) / (len(other.position - self.position) ** 2)

    def calculate_total_acceleration(self, others):
        return sum([self.calculate_attraction(body) for body in others])

    def step(self, others):
        self.acceleration = self.calculate_total_acceleration(others)
        self.velocity += self.acceleration * CONSTANTS["period"]
        self.position += self.velocity * CONSTANTS["period"] + (self.acceleration * CONSTANTS["period"] ** 2) / 2

