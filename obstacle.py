import pygame
import numpy as np


colour = 51,25,0
class Obstacle:
    def __init__(self, x, size, GroundHeight):
        self.x = x
        self.size = size
        self.GroundHeight = GroundHeight
        self.collided = False # Avoid multiple collistions with same object
        self.passed = False

    def draw(self, gameDisplay):
        pygame.draw.rect(gameDisplay, colour, [self.x, self.GroundHeight-self.size, self.size, self.size])

    def update(self, deltaTime, velocity):
        self.x -= velocity*deltaTime

    def checkOver(self):
        if self.x < 0:
            return True
        else:
            return False
        
    def reset(self, x, size, GroundHeight):
        self.x = x
        self.size = size
        self.GroundHeight = GroundHeight
        self.collided = False
        self.passed = False
        
        

class ObstaclePool:
    def __init__(self, initial_size, width, GROUND_HEIGHT, MINGAP, MAXGAP, VELOCITY, game_display=None):
        lastObstacle = width
        lastObstacle += MINGAP+(MAXGAP-MINGAP)*np.random.uniform(0, 1)
        #print("lastObstacle ="+str(lastObstacle))
    
        obstaclesize = 50*np.random.normal(loc=0.75, scale=0.5)
        self.pool = [Obstacle(lastObstacle, obstaclesize, GROUND_HEIGHT) for _ in range(initial_size)]
        self.game_display = game_display
        self.active = []

        self.lastObstacle = lastObstacle
        self.VELOCITY = VELOCITY
        self.GROUND_HEIGHT = GROUND_HEIGHT
        self.MINGAP = MINGAP
        self.MAXGAP = MAXGAP
    
    def get_obstacle(self):
        if self.pool:
            obs = self.pool.pop(0)
        else:
            return Obstacle(random.randint(600, 800), 50, self.GROUND_HEIGHT)
        self.active.append(obs)
        return obs

    def reset_obstacle(self, obs, deltaTime):
        self.lastObstacle += self.lastObstacle - self.VELOCITY*deltaTime
        new_size = 50 * np.random.normal(loc=0.5, scale=0.1)  # Adjust the new size as needed
        # Reset the obstacle with updated values
        newLastObstavle =  self.MINGAP+(self.MAXGAP-self.MINGAP)*np.random.uniform(0.4, 1)
        #print("lastObstacle ="+str(newLastObstavle))
        obs.reset(newLastObstavle, new_size, self.GROUND_HEIGHT)  
        obs.collided = False
        self.passed = False
        self.active.remove(obs)
        self.pool.append(obs)