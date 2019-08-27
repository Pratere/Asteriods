import pyglet
from game import resources, load, physicalobject, player, death_screen, model, asteroid
from pyglet.window import key

window_width = 800
window_height = 600
game_window = pyglet.window.Window(window_width, window_height)

main_batch = pyglet.graphics.Batch()
death_batch = pyglet.graphics.Batch()

score_label = pyglet.text.Label(x=10, y=window_height-25, batch=main_batch)
level_label = pyglet.text.Label(text="My Amazing Game",
                                x=window_width//2, y=window_height-25, anchor_x='center', batch=main_batch)

frame_counter = 0

def create_objects():
    player_ship = player.Player(x=window_width//2, y=window_height//2, batch=main_batch)
    game_window.push_handlers(player_ship)
    game_window.push_handlers(player_ship.key_handler)

    asteroids = load.asteroids(3, player_ship.position, batch=main_batch)

    game_objects = [player_ship] + asteroids

    return player_ship, game_objects

def update(dt):
    global player_ship
    global game_objects
    global death_labels
    global frame_counter
    astr_info = []
    for obj in game_objects:
        if isinstance(obj, asteroid.Asteroid):
            astr_info.append(obj.x)
            astr_info.append(obj.y)
            astr_info.append(obj.velocity_x)
            astr_info.append(obj.velocity_y)
    trainer.move(astr_info)
    for i in range(len(game_objects)):
        for j in range(i+1, len(game_objects)):
            obj_1 = game_objects[i]
            obj_2 = game_objects[j]
            if not obj_1.dead and not obj_2.dead:
                if obj_1.collides_with(obj_2):
                    obj_1.handle_collision_with(obj_2)
                    obj_2.handle_collision_with(obj_1)
    score_label.text = "Score: {0}".format(player_ship.score)
    to_add = []
    for obj in game_objects:
        obj.update(dt)
        to_add.extend(obj.new_objects)
        obj.new_objects = []

    if player_ship.dead:
        player_ship.restart = True
        # death_labels = death_screen.showDeathScreen(player_ship.score, death_batch, window_width, window_height)
        for to_remove in game_objects:
            to_remove.delete()
            game_objects.remove(to_remove)
    else:
        for to_remove in [obj for obj in game_objects if obj.dead]:
            to_remove.delete()
            game_objects.remove(to_remove)

    game_objects.extend(to_add)

    if player_ship.restart:
        # if not death_labels == None:
        #     for label in death_labels:
        #         label.delete()
        #         death_labels.remove(label)
        for to_remove in game_objects:
            to_remove.delete()
            game_objects.remove(to_remove)
        player_ship, game_objects = create_objects()
        trainer.player = player_ship
        trainer.replay(True)

    astr_info = []
    for obj in game_objects:
        if isinstance(obj, asteroid.Asteroid):
            astr_info.append(obj.x)
            astr_info.append(obj.y)
            astr_info.append(obj.velocity_x)
            astr_info.append(obj.velocity_y)

    trainer.remember(astr_info)

    frame_counter += 1
    if frame_counter % 10 == 0:
        trainer.replay()
    # if frame_counter == 120:
    #     pyglet.app.event_loop.exit()

@game_window.event
def on_draw():
    game_window.clear()
    resources.background_image.blit(0,0)
    main_batch.draw()
    death_batch.draw()


if __name__ == '__main__':
    player_ship, game_objects = create_objects()
    trainer = model.Agent(player_ship)
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
