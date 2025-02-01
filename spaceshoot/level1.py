import pygame
import sys
from gamelogic import maingame

pygame.init()

# Set up the display
screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption("Game Instructions")

# Define colors
color = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'button_color': (100, 100, 100),
    'hover_color':(70,70,200),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
}


# Set up font with a specific style
font = pygame.font.SysFont('Comic Sans MS', 40)
button_font = pygame.font.SysFont('Comic Sans MS', 30)

# Render the text
text1 = font.render("Reach a score of 15", True, color['white'])
text2 = font.render("to win the game!", True, color['white'])
button_text = button_font.render('OK', True, color['black'])

# Button dimensions
button_rect = pygame.Rect(350, 500, 200, 60)

# mouse cursors 
hand_cursor = pygame.image.load('assests/hand_cursar.png')
hand_cursor = pygame.transform.scale(hand_cursor,(20,20))
cursor = pygame.cursors.Cursor((0,0),hand_cursor)

arrow_cursor = pygame.cursors.arrow

pygame.mouse.set_visible(True)
maingame.gameloop_sound.play()
# Main loop
def gameloop():
    start = True
    while start:
        mouse_x,mouse_y = pygame.mouse.get_pos()

        is_howered = button_rect.collidepoint(mouse_x,mouse_y)

        Key = pygame.key.get_pressed()
        if Key[pygame.K_KP_ENTER]:
            is_howered = True
            start = False
            maingame.gameloop_sound.stop()
            maingame.gamestart.play()
            maingame.gameloop()

        pygame.mouse.set_cursor(*cursor) if is_howered else pygame.mouse.set_cursor(*arrow_cursor)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    start = False
                    pygame.mouse.set_visible(False)
                    pygame.mouse.set_cursor(*arrow_cursor)
                    maingame.gameloop()
            

        # Fill the screen with black
        screen.fill(color['black'])

        # Blit the text onto the screen
        screen.blit(text1, (screen.get_width() // 2 - text1.get_width() // 2, screen.get_height() // 2 - 50))
        screen.blit(text2, (screen.get_width() // 2 - text2.get_width() // 2, screen.get_height() // 2))

        # Draw the button
        pygame.draw.rect(screen,color['hover_color'] if is_howered else color['button_color'] , button_rect, border_radius=10)
        screen.blit(button_text, (button_rect.x + 75, button_rect.y + 15))

        # Update the display
        pygame.display.update()

if __name__ == "__main__":
    gameloop()