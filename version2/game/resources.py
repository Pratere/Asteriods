import pyglet

pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

asteroid_image = pyglet.resource.image('pixelated-asteroid-1.png')
asteroid_image.width = 50
asteroid_image.height = 50

player_image = pyglet.resource.image('ship.png')
player_image.width = 50
player_image.height = 50

engine_image = pyglet.resource.image('engine_flame.jpg')
engine_image.width = 45
engine_image.height = 35

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

center_image(player_image)
center_image(asteroid_image)
engine_image.anchor_x = engine_image.width * 1.5
engine_image.anchor_y = engine_image.height / 2
