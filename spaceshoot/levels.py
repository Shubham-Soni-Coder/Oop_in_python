import pygame 
from level1 import color
pygame.init()

class Game:
    def __init__(self, width=900, height=700):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simple Pygame Window")
        self.running = True
        pygame.mouse.set_visible(True)
        self.levels = Levels(self.width,self.height,self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx,my = pygame.mouse.get_pos()
                for i,(x,y) in enumerate(self.levels.button_position):
                    if (x-mx) ** 2 + (y-my) ** 2 <=self.levels.Button_Size **2 and self.levels.levels[i]==1:
                        print("Button Clicked")

    def run(self):
        while self.running:
            self.handle_events()
            self.levels.draw()
            
            pygame.display.flip()
    def __call__(self, width=900, height=700):
        self.width = width
        self.height = height
        # This method allows the instance to be called 
        # like a function to update width and height.


class Levels:
    def __init__(self,width,heigth,screen):

        self.width = width
        self.height = heigth
        self.screen = screen
        self.Border_Margin = 50
        #FOnts 
        self.nunber_font = pygame.font.Font(None,50)
        self.title_font = pygame.font.Font(None,70)

        # Level Data 1:Unlocked and 2:locked
        self.levels = [1,0,0,0,0,0,0,0,0]

        # Button of levels
        self.Button_Rows,self.Button_Column = 3,3
        self.Button_Size = 40
        self.space = 100
        self.start_x = self.width // 2 - (self.Button_Column - 1) *  self.space //2 
        self.start_y = self.height // 2 - (self.Button_Rows - 1) * self.space //2 + 50 
        self.button_position = [(self.start_x + (i % self.Button_Column) * self.space,
                                 self.start_y + (i // self.Button_Rows) * self.space)
                                 for i in range(len(self.levels))]
    def draw(self):

        # Draw border
        pygame.draw.rect(self.screen,color['blue'],
                        (self.Border_Margin,self.Border_Margin,
                        self.width -2 * self.Border_Margin,self.height-2 * self.Border_Margin),5)                            

        # Draw title banner
        title_rect = pygame.Rect(self.width//2- 150 ,self.Border_Margin - 20 , 300 ,60)
        pygame.draw.rect(self.screen,color['Dark_blue'],title_rect, border_radius=15)
        pygame.draw.rect(self.screen,color['blue'],title_rect,3 , border_radius= 15)

        # Draw title text 
        title_text = self.title_font.render("LEVELS", True, color['white'])
        self.screen.blit(title_text,(title_rect.x + 50 ,title_rect.y + 10))

        # Draw Button 
        for i,(x,y) in enumerate(self.button_position):
            self.color = color['green'] if self.levels[i] == 1 else color['red']
            pygame.draw.circle(self.screen,self.color,(x,y),self.Button_Size)
            pygame.draw.circle(self.screen, color['black'], (x, y), self.Button_Size + 2, 3)
            text = self.title_font.render(str(i+1),True,color['black'])
            self.screen.blit(text,(x-15,y-20))

if __name__ == "__main__":
    game = Game(width=900,height=700)
    game.run()

