import pygame
import sys
import math 
# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('bgscroll')

clock = pygame.time.Clock()
fps  = 60 

img1 = pygame.image.load('assests/bg2.jpg').convert()
img1 = pygame.transform.scale(img1,(width,height//2+100))

# game variable 
scroll = 0 
titles = math.ceil(height / img1.get_height()) + 2
speed = 1 
print(titles)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                speed  = 0     
            if event.key == pygame.K_q:
                speed = 1     

    # Fill the screen with a color (e.g., black)
    for i in range(0,titles):
        screen.blit(img1,(0,i*img1.get_height() + scroll))

    # change the scroll 
    scroll -= 5 * speed
    if abs(scroll) >= img1.get_height():
        scroll = 0 


    # Update the display
    clock.tick(fps)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
