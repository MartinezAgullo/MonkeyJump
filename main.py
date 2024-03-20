import pygame
import random
import sys, os
import psutil 

from monkey import Monkey
from obstacle import Obstacle, ObstaclePool
from peanut import Peanut



def main():
  pygame.init() #this ‘starts up’ pygame

  font = pygame.font.SysFont(None, 36)
  size = width,height = 960, 720
  gameDisplay= pygame.display.set_mode(size) #creates screen
  pygame.display.set_caption("Monkey Game")


  GROUND_HEIGHT = height-100
  MINGAP = 400
  VELOCITY = 300
  MAXGAP = 1200

  bkg_image_victory = '/Users/pablo/Desktop/Dino/Sprites/campello.jpeg'
  bkg_image = '/Users/pablo/Desktop/Dino/Sprites/jungle.jpeg'
  if os.path.exists(bkg_image):
      backgroundImage = pygame.image.load(bkg_image).convert()
      backgroundImage = pygame.transform.scale(backgroundImage, (960, 720))
  if os.path.exists(bkg_image_victory):
      backgroundImage_exito = pygame.image.load(bkg_image_victory).convert()
      backgroundImage_exito = pygame.transform.scale(backgroundImage_exito, (960, 720))

 
 # obstacles = []
 # num_of_obstacles = 4
 # lastObstacle = width
 # obstaclesize = 50
 # for i in range(num_of_obstacles):
#	  lastObstacle += MINGAP+(MAXGAP-MINGAP)*random.random() #Make distance between rocks random
#	  obstacles.append(Obstacle(lastObstacle, obstaclesize, GROUND_HEIGHT))
  
  obstacle_pool = ObstaclePool(5, width, GROUND_HEIGHT, MINGAP, MAXGAP, VELOCITY, gameDisplay)
  obstacles = [obstacle_pool.get_obstacle() for _ in range(4)]  # Start with 4 obstacles

     
  Monito = Monkey(GROUND_HEIGHT)
  MariscoMono = Peanut(GROUND_HEIGHT)
  peanut_time = 6

  lastFrame = pygame.time.get_ticks() #get ticks returns current time in milliseconds

  white = 255,255,255
  black = 0,0,0
  hierba = 102,204,0
  cielo = 51,255,255
  xPos = 0
  yPos = 0

  SCORE = 0

  running = True
  while running: #gameLoop it draws the frames of the game

    # Manage deltaTime
    t = pygame.time.get_ticks() 
    deltaTime = (t-lastFrame)/1000.0 
    lastFrame = t 

    for event in pygame.event.get(): #Check for events
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.KEYDOWN: #If user uses the keyboard
        if event.key == pygame.K_SPACE: #If that key is space
          Monito.jump() #Make monito jump
    if os.path.exists(bkg_image):
      gameDisplay.blit(backgroundImage, (0, 0))
    else:
      gameDisplay.fill(cielo)
    Monito.update(deltaTime)
    Monito.draw(gameDisplay)

    for obs in obstacles:
      obs.update(deltaTime, VELOCITY)
      obs.draw(gameDisplay)
      if obs.checkOver():
        if t / 1000.0 < (peanut_time-5):
          obstacle_pool.reset_obstacle(obs, deltaTime)
          obstacles.remove(obs)
          obstacles.append(obstacle_pool.get_obstacle())  
      
      # Update obstacle's rectangle for accurate collision detection
      obs_rect = pygame.Rect(obs.x, GROUND_HEIGHT-obs.size, obs.size, obs.size)

      if t / 1000.0 > peanut_time:
        MariscoMono.update(deltaTime, VELOCITY)
        #MariscoMono_rec = pygame.Rect(MariscoMono.x, GROUND_HEIGHT-MariscoMono.size, MariscoMono.size, MariscoMono.size)
        MariscoMono.draw(gameDisplay)

      if (MariscoMono.x < -1000) or (Monito.rect.colliderect(MariscoMono.rect)): # FIN PARTIDA
        if not (Monito.rect.colliderect(MariscoMono.rect)): 
          display_victory_text(gameDisplay, font, "meh")
          gameDisplay.fill(cielo)
        if (Monito.rect.colliderect(MariscoMono.rect)): 
          gameDisplay.blit(backgroundImage_exito, (0, 0))
          display_victory_text(gameDisplay, font, "Victory!")
        Monito.mono_feliz()
        MariscoMono.draw(gameDisplay)
        Monito.draw(gameDisplay)
        waiting_for_input = True
        while waiting_for_input:
          for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE:  # Press SPACE to restart or continue
                waiting_for_input = False
              elif event.key == pygame.K_RETURN:  # Press ESC to quit
                waiting_for_input = False
                running = False
            elif event.type == pygame.QUIT:
              waiting_for_input = False
              running = False
      # Check for collision
      #Monito.update(deltaTime)  # Assuming this updates Monito.y
      Monito.rect.y = GROUND_HEIGHT - Monito.y - 50

      #pygame.draw.rect(gameDisplay, (255, 0, 0), Monito.rect, 2) 
      #pygame.draw.rect(gameDisplay, (0, 255, 0), obs_rect, 2) 
      #pygame.draw.rect(gameDisplay, (0, 255, 0), MariscoMono.rect, 2) 
      if Monito.rect.colliderect(obs_rect) and not obs.collided:
          SCORE -= 5
          obs.collided = True
          print("Collision Detected! Score: ", SCORE)
        
      # Check if obstacle has passed beyond the left edge of the screen
      #if obs.x + obs.size < 0 and not obs.passed:
      if not Monito.rect.colliderect(obs_rect) and not obs.passed:
        obs.passed = True  # Mark as passed to prevent multiple score increments
        SCORE += 1
        print("Obstacle Passed! Score: ", SCORE)

    
    pygame.draw.rect(gameDisplay,hierba, [0,GROUND_HEIGHT, width, height-GROUND_HEIGHT]) # ground
    xPos += 1
    yPos += 1

    score_text = font.render('Score: ' + str(SCORE), True, (0, 0, 0))  # Render the score text in black
    gameDisplay.blit(score_text, (10, 10)) 

     # Get CPU and memory usage
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    
    # Prepare text surfaces
    # Prepare text surfaces with black color
    cpu_text = font.render(f'CPU Usage: {cpu_usage}%', True, pygame.Color('black'))
    memory_text = font.render(f'Memory Usage: {memory_usage}%', True, pygame.Color('black'))
    cpu_text_x = width - cpu_text.get_width() - 10  # 10 pixels margin
    memory_text_x = width - memory_text.get_width() - 10  # 10 pixels margin 
    
    # Blit text surfaces to the screen
    gameDisplay.blit(cpu_text, (cpu_text_x, 10))
    gameDisplay.blit(memory_text, (memory_text_x, 30))

    pygame.display.update()

  pygame.quit()
  sys.exit()



def display_victory_text(gameDisplay, font, text):
    victory_text = font.render(text, True, (255, 255, 255), (0, 0, 0))
    text_rect = victory_text.get_rect(center=(960/2, 720/2))  # Center text
    gameDisplay.blit(victory_text, text_rect)
    pygame.display.update() 


main()