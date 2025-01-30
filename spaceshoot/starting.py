import pygame
import sys
from main import maingame

pygame.init()


# Set up the display

screen = pygame.display.set_mode((900,700))
pygame.display.set_caption("Game Instructions")



# Define colors
color = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'grey': (100, 100, 100),
    'red': (255,0,0),
    'blue': (0,0,255),
    'green': (0,255,0),
}

# Set up font with a specific style
font = pygame.font.SysFont('Comic Sans MS', 40)
button_font = pygame.font.SysFont('Comic Sans MS', 30)

# Render the text
text1 = font.render("Reach a score of 30", True, color['white'])
text2 = font.render("to win the game!", True, color['white'])
button_text = button_font.render('OK', True, color['black'])

# Button dimensions
button_rect = pygame.Rect(200, 300, 200, 60)
# Main loop
def gameloop():
    start= True
    while start:

        mouse_pos = pygame.mouse.get_pos()

        if button_rect.collidepoint(mouse_pos):
            button_col = 'green'    
        else :
            button_col = 'gray'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    start = False
                    maingame.gameloop()

        # Fill the screen with black
        screen.fill(color['black'])

        # Blit the text onto the screen
        screen.blit(text1, (100, 150))
        screen.blit(text2, (150, 200))

        # Draw the button
        pygame.draw.rect(screen, button_col , button_rect, border_radius=10)
        screen.blit(button_text, (button_rect.x + 80, button_rect.y + 15))

        # Update the display
        pygame.display.update()

if __name__=="__main__":
    gameloop()