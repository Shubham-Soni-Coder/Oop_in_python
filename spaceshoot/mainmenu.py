import pygame
import sys
from levels import game, color

# Initialize Pygame globally
pygame.init()

class MainMenu:
    def __init__(self, width=game.width, heigth=game.height):
        self.width = width
        self.height = heigth

        # Set up display
        self.width = 1200
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Main Menu")
        # Set up font
        self.font = pygame.font.SysFont('Arial', 74)
        self.button_font = pygame.font.SysFont(None, 50)

        # Render text
        self.title_text = self.font.render('Main Menu', True, color['white'])
        self.title_rect = self.title_text.get_rect(center=(self.width // 2, 100))
        self.play_text = self.button_font.render('Play', True, color['white'])
        self.options_text = self.button_font.render('Options', True, color['white'])
        self.exit_text = self.button_font.render('Exit', True, color['white'])

        # Button positions (bottom left side of the screen)
        self.play_button = pygame.Rect(50, self.height - 250, 200, 50)
        self.options_button = pygame.Rect(50, self.height - 180, 200, 50)
        self.exit_button = pygame.Rect(50, self.height - 110, 200, 50)

        # Import image
        self.bg = pygame.image.load('assets/space.jpg')
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))

    def run(self):
        start = True
        while start:
            self.screen.fill(color['black'])
            self.screen.blit(self.bg, (0, 0))
            pos = pygame.mouse.get_pos()
            is_howered1 = self.play_button.collidepoint(pos)
            is_howered2 = self.options_button.collidepoint(pos)
            is_howered3 = self.exit_button.collidepoint(pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if is_howered1:  # check pos of play game
                        game.run()
                        start = False
                    elif is_howered2:  # check pos of options
                        print("Options")  # Placeholder for options menu
                    elif is_howered3:  # exit howered
                        running = False

            # cursor change logic
            if is_howered1 or is_howered2 or is_howered3:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            # Draw text
            self.screen.blit(self.title_text, self.title_rect)
            pygame.draw.rect(self.screen, color['hover_color'] if is_howered1 else color['button_color'], self.play_button)
            pygame.draw.rect(self.screen, color['hover_color'] if is_howered2 else color['button_color'], self.options_button)
            pygame.draw.rect(self.screen,color['hover_color'] if is_howered3 else color['button_color'], self.exit_button)
            self.screen.blit(self.play_text, (self.play_button.x + 50, self.play_button.y + 10))
            self.screen.blit(self.options_text, (self.options_button.x + 20, self.options_button.y + 10))
            self.screen.blit(self.exit_text, (self.exit_button.x + 60, self.exit_button.y + 10))

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
        sys.exit()

main_menu = MainMenu()
if __name__ == "__main__":
    main_menu.run()
    