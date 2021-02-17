from utils import *

class Boid:
    def __init__(self, sprite):
        self.sprite = sprite
        self.max_force = 1
        self.max_speed = 4
        self.crowd_distance = 50
        self.vision_radius = 100
        self.action_radius = 150
        self.attacking = True
        self.evading = False


# Steer towards the average heading of local flockmates
    def align(self, boids):
        steering = [0, 0]
        # Iterate through all boids
        for boid in boids:
            steering = sum(steering, boid.sprite.get_vel())
        if (len(boids) > 0):
            # Steering = desired vel - current actual velocity
            steering = div(steering, len(boids))
            steering = setMag(steering, self.max_speed)  # go in direction of neighbours but at max speed
            steering = sub(steering, self.sprite.get_vel())
            steering = limit(steering, self.max_force)  # control overall power
        return steering


# Steer to move toward the average position of local flockmates
    def cohesion(self, boids):
        steering = [0, 0]
        for boid in boids:
            steering = sum(steering, boid.sprite.get_pos())    
        if (len(boids) > 0):
            steering = div(steering, len(boids))
            steering = sub(steering, self.sprite.get_pos())
            steering = setMag(steering, self.max_speed)  
            steering = sub(steering, self.sprite.get_vel())
            steering = limit(steering, self.max_force) 
        return steering


# Steer to avoid crowding local flockmates
# 1. Get vector that points away from the local flockmate
# 2. Make it inversely proportional to the distance
# 3. Add it up
    def separation(self, boids):
        steering = [0, 0]
        for boid in boids:
            d = dist(self.sprite.get_pos(), boid.sprite.get_pos())
            if(d < self.crowd_distance):
                diff = sub(self.sprite.get_pos(), boid.sprite.get_pos()) 
                diff = mult(diff, 1 / d) # inverse proportion
                # the farther it is, the lower the magnitude should be
                steering = sum(steering, diff)
        if (len(boids) > 0):
            steering = div(steering, len(boids) ) 
            steering = setMag(steering, self.max_speed)  
            steering = sub(steering, self.sprite.get_vel())
            steering = limit(steering, self.max_force) 
        return steering


    def evade(self, boids, target):
        total = 0
        steering = [0, 0]
        for boid in boids:
            for t in target:
                d = dist(self.sprite.get_pos(), t.get_pos())
                if(d < self.action_radius):
                
                    diff = sub(self.sprite.get_pos(), t.get_pos()) 
                    diff = mult(diff, 1 / d) # inverse proportion
                    # the farther it is, the lower the magnitude should be
                    steering = sum(steering, diff)
                    total += 1
        if (total > 0):
            steering = div(steering, total) 
            steering = setMag(steering, self.max_speed)  
            steering = sub(steering, self.sprite.get_vel())
            steering = limit(steering, self.max_force) 
        return steering


    def evade_opt(self, boids, target):
        steering = [0, 0]
        for boid in boids:
            for t in target:
                d = dist(self.sprite.get_pos(), t.get_pos())
                diff = sub(self.sprite.get_pos(), t.get_pos()) 
                diff = mult(diff, 1 / d) # inverse proportion
                # the farther it is, the lower the magnitude should be
                steering = sum(steering, diff)
        if (len(boids) > 0):
            steering = div(steering, len(boids)) 
            steering = setMag(steering, self.max_speed)  
            steering = sub(steering, self.sprite.get_vel())
            steering = limit(steering, self.max_force) 
        return steering


    def attack(self, boids, targets):
        steering = [0, 0]
        for boid in boids:
            for t in targets:
                steering = sum(steering, t.get_pos())    
        if (len(boids) > 0):
            steering = div(steering, len(boids))
            steering = sub(steering, self.sprite.get_pos())
            steering = setMag(steering, self.max_speed)  
            steering = sub(steering, self.sprite.get_vel())
            steering = limit(steering, self.max_force) 
        return steering


    def get_neighbors(self, boids):
        neighbors = set([])
        for boid in boids:
            if boid != self:
                d = dist(self.sprite.get_pos(), boid.sprite.get_pos())
                if d < self.vision_radius:
                    neighbors.add(boid)
        return neighbors


    def get_boids_for_action(self, boids, targets):
        boids_for_action = set([])
        for boid in boids:
            for t in targets:
                d = dist(self.sprite.get_pos(), t.get_pos())
                if d < self.action_radius:
                    boids_for_action.add(boid)
        return boids_for_action

    def flock(self, boids, targets):
        # At every moment start with 0 acc and ann all forces to get new acc 
        self.sprite.acceleration = [0, 0] 

        neighbors = self.get_neighbors(boids)

        # Flocking
        alignment = self.align(neighbors)
        cohesion = self.cohesion(neighbors)
        separation = self.separation(neighbors)

        alignment = mult(alignment, 0.8)
        cohesion = mult(cohesion, 1.2)
        separation = mult(separation, 1.5)

        # Force accumulation
        self.sprite.acceleration = sum(self.sprite.acceleration, alignment)
        self.sprite.acceleration = sum(self.sprite.acceleration, cohesion)
        self.sprite.acceleration = sum(self.sprite.acceleration, separation)


        # Attacking
        if(self.attacking):
            boids_for_action = self.get_boids_for_action(boids, targets)
            attack = self.attack(boids_for_action, targets)
            attack = mult(attack, 1.5)
            self.sprite.acceleration = sum(self.sprite.acceleration, attack)

        # Evasion
        if(self.evading):
            boids_for_action = self.get_boids_for_action(boids, targets)
            evasion = self.evade_opt(boids_for_action, targets)
            evasion = mult(evasion, 1)
            self.sprite.acceleration = sum(self.sprite.acceleration, evasion)