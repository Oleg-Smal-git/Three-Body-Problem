import datetime

import physics
import pyglet
import config


def wrapper_generator():
    colors = [
        (255, 0, 0),  # red
        (0, 255, 0),  # green
        (0, 0, 255),  # blue
        (255, 255, 0),  # yellow
        (0, 255, 255),  # cyan
        (255, 0, 255),  # purple
    ]
    i = 0
    for c in colors:
        i += 1
        yield {
            "color": c,
            "name": f"Body_{i}"
        }
    while True:
        i += 1
        yield {
            "color": (255, 255, 255),  # white
            "name": f"Body_{i}"
        }


body_wrappers = wrapper_generator()


class BodyWrapper:
    def __init__(self, body=physics.Body(), color=None, name=None):
        if (
            isinstance(body, physics.Body) and
            (isinstance(color, tuple) or color is None) and
            (isinstance(name, str) or name is None)
        ):
            self.body = body
            self.color = color
            self.name = name
            self.wake = []
            if (self.color is None) or (self.name is None):
                wrapper = next(body_wrappers)
                self.color = self.color if self.color else wrapper["color"]
                self.name = self.name if self.name else wrapper["name"]

        else:
            raise TypeError(
                f"Incompatible argument types: " +
                f"body: {type(body)}, color: {type(color)}, " +
                f"name: {type(name)}"
            )

    def draw(self, origin=physics.Vector()):
        if isinstance(origin, physics.Vector):
            for trace in self.wake:
                pass
                pyglet.shapes.Circle(
                    x=trace.x + origin.x,
                    y=trace.y + origin.y,
                    radius=0.5,
                    color=self.color
                ).draw()
            pyglet.shapes.Circle(
                x=self.body.position.x + origin.x,
                y=self.body.position.y + origin.y,
                radius=2.5,
                color=self.color
            ).draw()
        else:
            raise TypeError(f"Incompatible argument type: {type(origin)}")


class Simulation:
    def __init__(self, wrappers=None):
        if wrappers is None:
            wrappers = []
        if isinstance(wrappers, list):
            self.wrappers = wrappers
            self.window = pyglet.window.Window(fullscreen=True)
        else:
            raise TypeError(f"Incompatible argument type: {type(wrappers)}")

    def draw(self, origin=physics.Vector()):
        if isinstance(origin, physics.Vector):
            for wrapper in self.wrappers:
                wrapper.draw(origin=origin)
        else:
            raise TypeError(f"Incompatible argument type: {type(origin)}")

    def update(self, dt):
        self.window.clear()
        for _ in range(config.CONSTANTS["calculation_scale"]):
            for i in range(len(self.wrappers)):
                self.wrappers[i].body.step(
                    delta_time=1 / (config.CONSTANTS["framerate"] * config.CONSTANTS["calculation_scale"]),
                    others=[self.wrappers[j].body for j in range(len(self.wrappers)) if j != i]
                )
        for i in range(len(self.wrappers)):
            self.wrappers[i].wake.append(
                physics.Vector(
                    x=self.wrappers[i].body.position.x,
                    y=self.wrappers[i].body.position.y
                )
            )
        self.draw(
            origin=physics.Vector(
                x=self.window.width / 2,
                y=self.window.height / 2
            )
        )

    def run(self):
        pyglet.clock.schedule_interval(
            func=self.update,
            interval=1 / config.CONSTANTS["framerate"]
        )
        pyglet.app.run()
