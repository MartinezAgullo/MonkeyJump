import pygame

MONKEYHEIGHT = 50
MONKEYWIDTH = 100
dinocolour = 255,255,255

class Monkey:
  def __init__(self, surfaceHeight):
    pygame.sprite.Sprite.__init__(self)
    
    self.x = 60
    self.y = 0
    self.yvelocity = 0
    self.height = MONKEYHEIGHT
    self.width = MONKEYWIDTH
    self.surfaceHeight = surfaceHeight

    self.jumps = 0  # Track the number of jumps
    self.doubleJumpTimer = 0  # Timer to track time between jumps
    self.canDoubleJump = False  # Flag to enable/disable double jump
        

    # Load Monkey sprite
    original_image = pygame.image.load('/Users/pablo/Desktop/Dino/Sprites/Monkey_1.png').convert_alpha()
    self.image = pygame.transform.scale(original_image, (MONKEYWIDTH, MONKEYHEIGHT))        
    self.rect = self.image.get_rect()
    self.rect.x = self.x
    self.rect.y = self.surfaceHeight - self.y - self.height
  
  def mono_feliz(self):
    happy_monkey  = pygame.image.load('/Users/pablo/Desktop/Dino/Sprites/Monkey_2.png').convert_alpha()
    self.image = pygame.transform.scale(happy_monkey, (MONKEYHEIGHT,MONKEYWIDTH))
    self.rect = self.image.get_rect()



  def jump(self): 
    if self.y == 0 or (self.canDoubleJump and self.jumps < 2 and self.doubleJumpTimer < 0.2): #Only allow jumping if on the ground
      self.yvelocity = 300
      self.jumps += 1
      if self.jumps == 1:
        self.canDoubleJump = True
        self.doubleJumpTimer = 0
              


  def update(self, deltaTime): 
    self.yvelocity += -500*deltaTime #Gravity
    self.y += self.yvelocity * deltaTime
    if self.y < 0: #if into the ground, make velocity and y = 0
      self.y = 0
      self.yvelocity = 0
      self.jumps = 0  # Reset jump counter when landing
      self.canDoubleJump = False
      if self.canDoubleJump:
            self.doubleJumpTimer += deltaTime


  def draw(self,display):
    display.blit(self.image, (self.x, self.surfaceHeight-self.y-self.height,self.width,self.height))
    #display.blit(self.image, (self.rect.x, self.surfaceHeight - self.rect.y - self.height))
    #display.blit(self.image, (self.rect.x, self.surfaceHeight  self.rect.y))
    #pygame.draw.rect(display,dinocolour,[self.x,self.surfaceHeight-self.y-self.height,self.width,self.height])
    #pygame.draw.rect(display,image)