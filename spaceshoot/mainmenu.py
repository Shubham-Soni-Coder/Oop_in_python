import pygame
import sys

# Initialize Pygame
pygame.init()

width = 900
height = 700

# Set up the display
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Main Menu")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Set up font
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Render text
title_text = font.render('Main Menu', True, WHITE)
play_text = button_font.render('Play', True, WHITE)
options_text = button_font.render('Options', True, WHITE)
exit_text = button_font.render('Exit', True, WHITE)

# Button positions
play_button = pygame.Rect(300, 200, 200, 50)
options_button = pygame.Rect(300, 300, 200, 50)
exit_button = pygame.Rect(300, 400, 200, 50)


# import iamge 
bg = pygame.image.load('assets/space.jpg')
bg = pygame.transform.scale(bg,(width,height))
# Main loop
running = True
while running:
    screen.fill(BLACK)
    screen.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos):
                print("Play Game")  # Placeholder for starting the game
            elif options_button.collidepoint(event.pos):
                print("Options")  # Placeholder for options menu
            elif exit_button.collidepoint(event.pos):
                running = False

    # Fill the screen with black

    # Draw text
    screen.blit(title_text, (250, 100))
    pygame.draw.rect(screen, GRAY, play_button)
    pygame.draw.rect(screen, GRAY, options_button)
    pygame.draw.rect(screen, GRAY, exit_button)
    screen.blit(play_text, (play_button.x + 50, play_button.y + 10))
    screen.blit(options_text, (options_button.x + 20, options_button.y + 10))
    screen.blit(exit_text, (exit_button.x + 60, exit_button.y + 10))

    # Update the display

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
