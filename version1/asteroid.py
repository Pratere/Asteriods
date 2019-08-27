import pyglet
from game import resources, load, physicalobject, player

game_window = pyglet.window.Window(800, 600)

main_batch = pyglet.graphics.Batch()

score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)
level_label = pyglet.text.Label(text="My Amazing Game",
                                x=400, y=575, anchor_x='center', batch=main_batch)

player_ship = player.Player(x=400, y=300, batch=main_batch)
game_window.push_handlers(player_ship)

player_lives = load.player_lives(3, main_batch)

asteroids = load.asteroids(3, player_ship.position, batch=main_batch)

game_objects = [player_ship] + asteroids

def update(dt):
    for obj in game_objects:
        obj.update(dt)

@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
