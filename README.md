# AI Lab2 - Flocking behavior (boids)
This porject contains implementation of laboratory work for Artificial Intelligence course (UTM 2021).

The task was to take an Asteroids game and implement flocking behavior for enemy units (asteroids). Units can also exhibit attacking or evading behavior, thrusting themselves into the player's ship or escaping it correspondingly

*Note: The code of the game is not uploaded. The repo contains only Boids behavior that is applied to the game as a 3rd party library*

# Approach

Since Asteroids is a 2D game, all the game mechanics are based on the 2D arrays transformations. Each unit has its own position P[x,y], velocity V[x,y] and acceleration A[x,y]. Position coordinates show where a unit is currently displayed on a map. Velocity affects position over time and also it is a vector that shows the direction towards which the unit is moving. From physics we know that velocity depends on acceleration, which is also a vector. To sum this up, modifying acceleration vectors of the units, we can easily affect their velocity and position consequently.

Utility functions for operation on 2D vectors can be found in *unitls.py*

## Python

In order to use this library, you shoud have your game impleted. Then just import *boid.py* in your game code and you are ready to go:
```bash
   import boid
  ```
In order to have access to flocking, evading and attacking behavior, you should wrap you game objects in Boid class. Boids behavior can be changed through the following methods:

* *align* - Steer towards the average heading of local flockmates
* *cohesion* - Steer to move toward the average position of local flockmates
* *separation* - Steer to avoid crowding local flockmates
* *evade* - Steer to avoid player's ship and missiles
* *attack* - Steer to move toward the player's ship and missiles
* *flock* - Apply *align*,*cohesion* and *separation* simultaneously

