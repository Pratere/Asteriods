import pyglet
import math
from pyglet.window import key
from . import physicalobject, resources, bullet, load


class Player(physicalobject.PhysicalObject):

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(img=resources.player_image, *args, **kwargs)
        self.thrust = 300.0
        self.rotate_speed = 200.0
        self.key_handler = key.KeyStateHandler()
        self.engine_sprite = pyglet.sprite.Sprite(img=resources.engine_image1, *args, **kwargs)
        self.engine_sprite.visible = False
        self.bullet_speed = 700.0
        self.reacts_to_bullets = False
        self.num_lives = 3
        self.lives = load.player_lives(self.num_lives, self.batch)
        self.score = 0
        self.restart = False
        self.actions = [False, False, False, False]

    def update(self, dt):
        super(Player, self).update(dt)

        # if self.key_handler[key.LEFT]:
        #     self.rotation -= self.rotate_speed * dt
        # if self.key_handler[key.RIGHT]:
        #     self.rotation += self.rotate_speed * dt
        # if self.key_handler[key.UP]:
        #     angle_radians = -math.radians(self.rotation)
        #     force_x = math.cos(angle_radians) * self.thrust * dt
        #     force_y = math.sin(angle_radians) * self.thrust * dt
        #     self.velocity_x += force_x
        #     self.velocity_y += force_y
        #     self.engine_sprite.rotation = self.rotation
        #     self.engine_sprite.x = self.x
        #     self.engine_sprite.y = self.y
        #     self.engine_sprite.visible = True

        if self.actions[0]:
            self.rotation -= self.rotate_speed * dt
        if self.actions[1]:
            self.rotation += self.rotate_speed * dt
        if self.actions[2]:
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.thrust * dt
            force_y = math.sin(angle_radians) * self.thrust * dt
            self.velocity_x += force_x
            self.velocity_y += force_y
            self.engine_sprite.rotation = self.rotation
            self.engine_sprite.x = self.x
            self.engine_sprite.y = self.y
            self.engine_sprite.visible = True

        else:
            self.engine_sprite.visible = False

        if self.actions[3]:
            self.fire()

    def on_key_press(self, symbol, modifiers):
        # if symbol == key.SPACE and not self.dead:
        #     self.fire()
        if symbol == key.R:
            self.restart = True

    def fire(self):
        angle_radians = -math.radians(self.rotation)
        ship_radius = self.image.width/2
        bullet_x = self.x + math.cos(angle_radians) * ship_radius
        bullet_y = self.y + math.sin(angle_radians) * ship_radius
        new_bullet = bullet.Bullet(self, bullet_x, bullet_y, batch=self.batch)
        bullet_vx = (
            self.velocity_x +
            math.cos(angle_radians) * self.bullet_speed
        )
        bullet_vy = (
            self.velocity_y +
            math.sin(angle_radians) * self.bullet_speed
        )
        new_bullet.velocity_x = bullet_vx
        new_bullet.velocity_y = bullet_vy
        new_bullet.rotation = self.rotation
        self.new_objects.append(new_bullet)

    def handle_collision_with(self, other_object):
        super(Player, self).handle_collision_with(other_object)
        if self.dead and len(self.lives) > 1:
            self.dead = False
            self.lives[-1].delete()
            self.lives = self.lives[0:-1]
            self.x, self.y = 400, 300
            self.velocity_x, self.velocity_y = 0.0, 0.0
            self.rotation = 0.0
        else:
            self.lives = None


    def delete(self):
        self.engine_sprite.delete()
        super(Player, self).delete()
