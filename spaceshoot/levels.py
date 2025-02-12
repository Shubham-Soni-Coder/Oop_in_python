import pygame 
import importlib
import tkinter as tk 
from tkinter import messagebox
import threading


pygame.init()
levels = {i:importlib.import_module(f"level{i}") for i in range(1,3)}

class Game:
    def __init__(self, width=levels[1].main.width, height=levels[1].main.height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simple Pygame Window")
        self.running = True
        pygame.mouse.set_visible(True)
        self.levels = Levels(self.width, self.height, self.screen)
        self.back_button_rect = pygame.Rect(self.width // 2 - 75, self.height - 120, 150, 50)

    @staticmethod
    def show_messagebox():
        '''Display a normal message box'''
        
        # tk window
        root = tk.Tk()
        root.withdraw()  # turn off the tk window 
        messagebox.showinfo("Message Box", "Complete Preview level first")
        
        root.destroy()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if self.back_button_rect.collidepoint(mx, my):
                    from mainmenu import main_menu
                    main_menu.run()
                for i, (x, y) in enumerate(self.levels.button_position):
                    if (x - mx) ** 2 + (y - my) ** 2 <= self.levels.Button_Size ** 2:
                        levels[i+1].main.main_loop() if self.levels.levels[i] == 1 else threading.Thread(target=self.show_messagebox,daemon=True).start()
    def update_cursor(self):
        mx, my = pygame.mouse.get_pos()
        mouse_over_button = False
        if self.back_button_rect.collidepoint(mx, my):
           mouse_over_button = True
        for _, (x, y) in enumerate(self.levels.button_position):
            if (x - mx) ** 2 + (y - my) ** 2 <= self.levels.Button_Size ** 2:
                mouse_over_button = True
        if mouse_over_button:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def run(self):
        while self.running:
            self.handle_events()
            self.update_cursor()
            self.levels.draw()
            self.draw_back_button()
            pygame.display.flip()

    def draw_back_button(self):
        pygame.draw.rect(self.screen, levels[1].color['red'], self.back_button_rect)
        pygame.draw.rect(self.screen, levels[1].color['black'], self.back_button_rect, 3)
        text = self.levels.title_font.render("Back", True, levels[1].color['black'])
        self.screen.blit(text, (self.back_button_rect.x + 20, self.back_button_rect.y + 5))

    def __call__(self, width=levels[1].main.width, height=levels[1].main.height):
        self.width = width
        self.height = height
        # This method allows the instance to be called 
        # like a function to update width and height.

class Levels:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.Border_Margin = 50
        # Fonts 
        self.number_font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 70)

        # Level Data 1: Unlocked and 2: Locked
        self.levels = [1, 0, 0, 0, 0, 0, 0, 0, 0]

        # Button of levels
        self.Button_Rows, self.Button_Column = 3, 3
        self.Button_Size = 40
        self.space = 100
        self.start_x = self.width // 2 - (self.Button_Column - 1) * self.space // 2 
        self.start_y = self.height // 2 - (self.Button_Rows - 1) * self.space // 2 + 50 
        self.button_position = [(self.start_x + (i % self.Button_Column) * self.space,
                                 self.start_y + (i // self.Button_Rows) * self.space)
                                 for i in range(len(self.levels))]

    def draw(self):
        # Draw border
        pygame.draw.rect(self.screen, levels[1].color['blue'],
                         (self.Border_Margin, self.Border_Margin,
                          self.width - 2 * self.Border_Margin, self.height - 2 * self.Border_Margin), 5)                            

        # Draw title banner
        title_rect = pygame.Rect(self.width // 2 - 150, self.Border_Margin - 20, 300, 60)
        pygame.draw.rect(self.screen, levels[1].color['Dark_blue'], title_rect, border_radius=15)
        pygame.draw.rect(self.screen, levels[1].color['blue'], title_rect, 3, border_radius=15)

        # Draw title text 
        title_text = self.title_font.render("LEVELS", True, levels[1].color['white'])
        self.screen.blit(title_text, (title_rect.x + 50, title_rect.y + 10))

        # Draw Button 
        for i, (x, y) in enumerate(self.button_position):
            self.color = levels[1].color['green'] if self.levels[i] == 1 else levels[1].color['red']
            pygame.draw.circle(self.screen, self.color, (x, y), self.Button_Size)
            pygame.draw.circle(self.screen, levels[1].color['black'], (x, y), self.Button_Size + 2, 3)
            text = self.number_font.render(str(i + 1), True, levels[1].color['black'])
            self.screen.blit(text, (x - 15, y - 20))

game = Game()
if __name__ == "__main__":
    game.run()

