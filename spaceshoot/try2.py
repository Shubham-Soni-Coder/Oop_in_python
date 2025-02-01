import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Toggle Mouse Visibility")

# Variable to track mouse visibility
mouse_visible = False
pygame.mouse.set_visible(mouse_visible)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                mouse_visible = not mouse_visible
                pygame.mouse.set_visible(mouse_visible)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw instructions (optional)
    font = pygame.font.SysFont(None, 36)
    text = font.render("Press Left Ctrl to toggle mouse visibility", True, (255, 255, 255))
    screen.blit(text, (50, 50))

    # Update the display
    pygame.display.flip()
