import pygame
import sys

pygame.init()

# Set up the display
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Game Instructions")

# Define colors
color = {
    'white': (255, 255, 255),
    'black': (0, 0, 0)
}

# Set up font with a specific style
font = pygame.font.SysFont('Comic Sans MS', 40)

# Render the text
text1 = font.render("Reach a score of 30", True, color['white'])
text2 = font.render("to win the game!", True, color['white'])

# Main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

    # Fill the screen with black
    screen.fill(color['black'])

    # Blit the text onto the screen
    screen.blit(text1, (100, 150))
    screen.blit(text2, (150, 200))

    # Update the display
    pygame.display.update()


