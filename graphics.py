from physics import Body, Vector
import pyglet
import datetime


def color_generator():
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255)
    ]
    for c in colors:
        yield c
    while True:
        yield 0, 0, 0


colors_list = color_generator()


class BodyWrapper:
    def __init__(self, body=Body()):
        self.body = body
        self.color = next(colors_list)
        self.trace = []

    def draw(self, origin):
        if self.trace:
            pyglet.graphics.draw(
                int(len(self.trace) / 2),
                pyglet.gl.GL_POINTS,
                ('v2f', self.trace),
            )
        pyglet.shapes.Circle(
            x=self.body.position.x + origin.x,
            y=self.body.position.y + origin.y,
            radius=10,
            color=self.color
        ).draw()


class BodyCluster:
    def __init__(self, wrappers=None):
        if wrappers is None:
            wrappers = list()
        self.bodies = wrappers

    def step(self, origin):
        for i in range(len(self.bodies)):
            next_position = self.bodies[i].body.step(
                others=[self.bodies[j].body for j in range(len(self.bodies)) if j != i]
            )
            self.bodies[i].trace.extend([
                next_position.x + origin.x,
                next_position.y + origin.y
            ])

    def draw(self, origin):
        for body in self.bodies:
            body.draw(origin)


class Game:
    def __init__(self, cluster=BodyCluster()):
        self.cluster = cluster
        self.window = pyglet.window.Window(
            fullscreen=True
        )

    def update(self, dt):
        self.window.clear()
        self.cluster.step(
            origin=Vector(
                x=self.window.width / 2,
                y=self.window.height / 2
            ))
        self.cluster.draw(
            origin=Vector(
                x=self.window.width / 2,
                y=self.window.height / 2
            )
        )

    def run(self):
        pyglet.clock.schedule_interval(self.update, 0.1)
        pyglet.app.run()
