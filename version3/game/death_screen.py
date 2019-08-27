import pyglet

def showDeathScreen(score, batch, window_width, window_height):
    deathScreen_label = pyglet.text.Label(text="You died!",
                                        x=window_width//2, y=window_height-50, anchor_x='center', batch=batch)
    final_score = pyglet.text.Label(text="You died!\nYour final score: {0}".format(score),
                                        x=window_width//2, y=window_height//2, anchor_x='center', anchor_y='center', batch=batch)
    continue_label = pyglet.text.Label(text="Press Enter to continue",
                                        x=window_width//2, y=25, anchor_x='center', batch=batch)
    labels = [continue_label, final_score, deathScreen_label]

    return labels
