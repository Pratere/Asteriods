from tensorflow.keras import *
import numpy as np
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
#
model = Sequential()
model.add(layers.Dense(10, activation='relu', input_dim=7))
model.add(layers.Dense(10, activation='relu'))
model.add(layers.Dense(7, activation='sigmoid'))
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

print(model.predict(np.array([[2, 3, 4, 8, 8, 0, 7],])))

# actions = [press_left, press_right, press_up, release_left, release_right, release_up, fire]

# vars = [asteriod.x, asteroid.y, asteroid.x_vel, asteroid.y_vel, asteroid.distance]
