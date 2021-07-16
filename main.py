import graphics
import physics


if __name__ == '__main__':
    graphics.Game(
        cluster=graphics.BodyCluster(
            [graphics.BodyWrapper(body) for body in [
                physics.Body(
                    position=physics.Vector(100, 100),
                    mass=1
                ),
                physics.Body(
                    position=physics.Vector(-100, 100),
                    mass=1
                ),
                physics.Body(
                    position=physics.Vector(100, -100),
                    mass=1
                )
            ]]
        )
    ).run()
