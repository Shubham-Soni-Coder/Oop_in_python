import pygame 
import sys

# Initialize Pygame
pygame.init()

class SimplePygameWindow:
    def __init__(self, width=1200, height=700):
        self.width = width
        self.height = height
        
        # Set up the display
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simple Pygame Window")
        
        # Define button properties
        self.button_font = pygame.font.Font(None, 48)  # Increased font size
        self.button_color = (255, 255, 255)
        self.button_hover_color = (100, 100, 100)
        self.button_texts = ["Settings", "About", "Back"]
        self.buttons = []
        
        # Create buttons
        for i, text in enumerate(self.button_texts):
            button_surface = self.button_font.render(text, True, self.button_color)
            button_rect = button_surface.get_rect(center=(self.width // 2, self.height // 2 - 50 + i * 60))
            self.buttons.append((button_surface, button_rect))
        
        # Define border properties
        self.border_color = (255, 255, 255)
        self.border_width = 2

    def check_button_click(self, mouse_pos):
        for i, (_, button_rect) in enumerate(self.buttons):
            if button_rect.collidepoint(mouse_pos):
                print(f"{self.button_texts[i]} button is clicked")

    def run(self):
        # Main game loop
        while True:
            mouse_over_button = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_button_click(event.pos)
            
            # Fill the screen with a color (e.g., black)
            self.screen.fill((0, 0, 0))
            
            # Draw buttons with borders and check for hover
            for i, (button_surface, button_rect) in enumerate(self.buttons):
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    mouse_over_button = True
                    pygame.draw.rect(self.screen, (0, 0, 0), button_rect.inflate(10, 10), self.border_width)
                    button_surface = self.button_font.render(self.button_texts[i], True, self.button_hover_color)
                else:
                    pygame.draw.rect(self.screen, self.border_color, button_rect.inflate(10, 10), self.border_width)
                    button_surface = self.button_font.render(self.button_texts[i], True, self.button_color)
                self.screen.blit(button_surface, button_rect)
            
            # Change cursor based on hover state
            if mouse_over_button:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            # Update the display
            pygame.display.flip()

if __name__ == "__main__":
    window = SimplePygameWindow()
    window.run()