# Example file showing a circle moving on screen
from cmath import rect
from tabnanny import check
from tkinter import CURRENT
from turtle import distance
import pygame
import random
import threading




# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
numParticles = 1000
simulate = True
particle_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
limiter = 0
particleSpeed = 1000;
particlesList = []
particleRadius = 60

mouseRadius = 100






currentTime = pygame.time.get_ticks()
update_time = pygame.time.get_ticks()
deltaTime = (currentTime - update_time)

intDeltaTime = (currentTime - update_time)

deltaTime=str(deltaTime)

pygame.font.init()

def randomParticleGeneration():  
    global limiter
    if intDeltaTime <= 0.02 and limiter <= 10000:
        limiter += 1
        print(limiter)
        r_value = random.randint(1,255)
        g_value = random.randint(1,255)
        b_value = random.randint(1,255)
        particleX = random.randint(1,1200)
        particleY = random.randint(1,1000)
        particleRadius = 10

        velocityX = random.uniform(-2,2)
        velocityY = random.uniform(-2,2)

        velocity = pygame.Vector2(velocityX,velocityY)
        particlePos = pygame.Vector2(particleX,particleY)
        pygame.draw.circle(screen,(r_value,g_value,b_value), particlePos, particleRadius)
        particlesList.append((particlePos,velocity,particleRadius,(r_value,g_value,b_value)))

       
def checkParticlePos(particlePos, velocity):
    # Print the value and type to debug
    print(f"particlePos: {particlePos}, type: {type(particlePos)}")
        
    
   
    if not isinstance(particlePos, pygame.Vector2):
        raise TypeError("particlePos should be a pygame.Vector2, got type: " + str(type(particlePos)))
    
    if particlePos.x >= 1280 or particlePos.x <= 0:
        velocity.x *= -1  # Reverse direction on X-axis
    if particlePos.y >= 720 or particlePos.y <= 0:
        velocity.y *= -1  # Reverse direction on Y-axis

    return velocity

def  checkForParticleCollision():
    for i, (pos1, vel1, radius1, color1) in enumerate(particlesList):
        for j, (pos2, vel2, radius2, color2) in enumerate(particlesList):
            if i != j:
                
                if (pos1 - pos2).length() <= (radius1 + radius2):  
                    
                    direction = pos2 - pos1
                    if direction.length() > 0: 
                        direction = direction.normalize()  
                    
                    # Calculate the distance to move based on the radii
                    distance_to_move = radius1 + radius2 + 10
                    
                    # Move pos1 and pos2 to ensure their edges meet
                    pos1 += direction * (distance_to_move / 2)  # Move pos1 away
                    pos2 -= direction * (distance_to_move / 2)  # Move pos2 away

                    vel1 = vel2


                    # Update the particles in the list
                    particlesList[i] = (pos1, vel1, radius1, color1)
                    particlesList[j] = (pos2, vel2, radius2, color2)  

            

def findRectBounds(particlePos):
    partCent = particlePos.x
    partLeft = particlePos.x - 30
    partWidth = 60
    partHeight = 60
    particlesList.append()

        
def mouseRepel(mouseRadius):
    mousePos = pygame.Vector2(pygame.mouse.get_pos())
    repelArea = mouseRadius 
    mousePressed = pygame.mouse.get_pressed()
    for i,(particlePos,particleVel,particleRadius,color) in enumerate(particlesList):
            distance_to_mouse = (particlePos - mousePos).length()
            
            if  distance_to_mouse <= repelArea and mousePressed[0]:
                particleVel = (particleVel * -2) 
                particlePos = pygame.Vector2(particlePos)
                particlesList[i] = (particlePos,particleVel,particleRadius,color)







def renderText(screen,text,font_size,color,position):
     # Initialize the font
    font = pygame.font.Font(None, font_size)
    
    # Render the text
    text_surface = font.render(text, True, color)
    
    # Blit the text to the screen at the given position
    screen.blit(text_surface, position)


while running:
   


    
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    randX = (random.randint(1,100))
    renderText(screen,rf"DeltaTime:{dt}",24,(255,255,255),(400,400)) 
    randomParticleGeneration()
    mouseRepel(300)

    for i, (particlePos, velocity,particleRadius,color) in enumerate(particlesList):
        particlePos += velocity
        velocity = checkParticlePos(particlePos,velocity)
        pygame.draw.circle(screen, color, (int(particlePos.x), int(particlePos.y)), particleRadius)

        particlesList[i] = (particlePos,velocity,particleRadius,color)

    
    checkForParticleCollision()
    mouseRepel(100)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

