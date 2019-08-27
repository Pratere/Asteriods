import pyglet
from . import physicalobject, resources


class Bullet(physicalobject.PhysicalObject):
    """Bullets fired by the player"""
    def __init__(self, player, *args, **kwargs):
        super(Bullet, self).__init__(
            resources.bullet_image, *args, **kwargs)
        pyglet.clock.schedule_once(self.die, 0.5)
        self.is_bullet = True
        self.player = player

    def die(self, dt):
        self.dead = True

    def handle_collision_with(self, other_object):
        super(Bullet, self).handle_collision_with(other_object)
        if self.dead:
            self.player.score += 1
