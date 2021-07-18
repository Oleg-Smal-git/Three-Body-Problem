import graphics
import physics


if __name__ == '__main__':
    graphics.Simulation(
        [
            graphics.BodyWrapper(body) for body in
            [
                physics.Body(
                    position=physics.Vector(100, 100),
                    mass=100
                ),
                physics.Body(
                    position=physics.Vector(-100, 100),
                    mass=100
                ),
                physics.Body(
                    position=physics.Vector(100, -100),
                    mass=100
                ),
                # physics.Body(
                #     position=physics.Vector(-100, -100),
                #     mass=100
                # ),
            ]
        ]
    ).run()

