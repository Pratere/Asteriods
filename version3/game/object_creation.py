import pyglet
from . import resources, load, physicalobject, player, death_screen

def create_objects():
    player_ship = player.Player(x=window_width//2, y=window_height//2, batch=main_batch)
    game_window.push_handlers(player_ship)
    game_window.push_handlers(player_ship.key_handler)

    asteroids = load.asteroids(3, player_ship.position, batch=main_batch)

    game_objects = [player_ship] + asteroids

    return player_ship, game_objects

def test_restart():
        if player_ship.restart:
            player_ship, game_objects = object_creation.create_objects()
        return create_objects()
