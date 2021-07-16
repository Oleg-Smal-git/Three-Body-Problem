from physics import Body
import pyglet


def colorGenerator():
    colors = ["red", "green", "blue"]
    for c in colors:
        yield c
    while True:
        yield "black"


colorsList = colorGenerator()


class BodyWrapper:
    def __init__(self, body):
        self.body = body
        self.colorName = next(colorsList)
        self.trace = []

    def draw(self):
        pass


class BodyCluster:
    def __init__(self, wrappers):
        self.bodies = list(wrappers)

    def draw(self):
        pass
