import pygame
import sys
from gamelogic import maingame

# Define colors
color = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'button_color': (100, 100, 100),
    'hover_color': (70, 70, 200),
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'Dark_blue':(0,0,155),
    'green': (0, 255, 0),
}

# Initialize pygame only once
pygame.init()   

class GameStart:
    def __init__(self,width=maingame.width,height=maingame.height):
        self.width = width
        self.height = height
        # Set up the display
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Game Instructions")

        # score variable 
        self.required_score = 15

        # Load images
        self.load_images()
        self.start = maingame

        # call all Function 
        self.setup_fonts()
        self.setup_cursors()
        self.setup_texts()
        self.setup_button()

    def load_images(self):
        try:
            self.hand_cursor_img = pygame.image.load('assets/image/hand_cursor.png')
        except FileNotFoundError:
            print("Error:hand cursor file not found")
            sys.exit(1)

    def setup_fonts(self):
        self.font = pygame.font.SysFont('Comic Sans MS', 40)
        self.button_font = pygame.font.SysFont('Comic Sans MS', 30)
 
    def setup_cursors(self):
        hand_cursor = pygame.transform.scale(self.hand_cursor_img, (20, 20))
        self.cursor = pygame.cursors.Cursor((0, 0), hand_cursor)
        self.arrow_cursor = pygame.cursors.arrow

    def setup_texts(self):
        self.text1 = self.font.render(f"Reach a score of {self.required_score}", True, color['white'])
        self.text2 = self.font.render("to win the game!", True, color['white'])
        self.button_text = self.button_font.render('OK', True, color['black'])

    def setup_button(self):
        self.button_rect = pygame.Rect(self.width // 2 - 100, self.height - 200, 200, 60)

    def start_game(self):
        pygame.mouse.set_visible(False)
        pygame.mouse.set_cursor(*self.arrow_cursor)
        self.start.gameloop()

    def main_loop(self):
        pygame.mouse.set_visible(True)
        maingame.gameloop_sound.play()
        self.run = True
        while self.run:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            is_hovered = self.button_rect.collidepoint(mouse_x, mouse_y)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        maingame.gameloop_sound.stop()
                        maingame.gamestart.play()
                        self.start_game()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_KP_ENTER]:
                is_hovered = True
                maingame.gameloop_sound.stop()
                maingame.gamestart.play()
                self.start_game()

            pygame.mouse.set_cursor(*self.cursor) if is_hovered else pygame.mouse.set_cursor(*self.arrow_cursor)

            # Fill the screen with black
            self.screen.fill(color['black'])

            # Blit the text onto the screen
            self.screen.blit(self.text1, (self.screen.get_width() // 2 - self.text1.get_width() // 2, self.screen.get_height() // 2 - 50))
            self.screen.blit(self.text2, (self.screen.get_width() // 2 - self.text2.get_width() // 2, self.screen.get_height() // 2))

            # Draw the button
            pygame.draw.rect(self.screen, color['hover_color'] if is_hovered else color['button_color'], self.button_rect, border_radius=10)
            self.screen.blit(self.button_text, (self.button_rect.x+75, self.button_rect.y + 15)) # draw ok in button 

            # Update the display
            pygame.display.update()

    def __call__(self,width=maingame.width,height=maingame.height):
        self.width = width
        self.height = height

main = GameStart()
if __name__=="__main__":
    main.main_loop()