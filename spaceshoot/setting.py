import pygame
import sys
class GameSettings:
    def __init__(self, width=800, height=600, settings=None):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game Settings")
        self.font = pygame.font.SysFont(None, 48)
        self.settings = settings if settings else {}
        self.running = True

    def draw_settings(self):
        self.screen.fill((0, 0, 0))
        y_offset = 50
        for setting_name in self.settings.keys():
            label = self.font.render(setting_name, True, (255, 255, 255))
            self.screen.blit(label, (50, y_offset))
            y_offset += 50
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.draw_settings()
        pygame.quit()

class resolution:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height

    def __str__(self):
        return f"{self.width}x{self.height}"
    def __repr__(self):
        return f"resolution({self.width}, {self.height})"
    




# Example usage:
if __name__ == "__main__":
    settings = {
        "Resolution": "800x600",
        "Fullscreen": "No",
        "Volume": "75",
    }
    game_settings = GameSettings(settings=settings)
    game_settings.run()
