import pygame 
import sys
from level1 import GameStart,color

pygame.init()

class maingame:
    def __init__(self,width=900,height=700):
        self.width = width
        self.height = height

        # set up display 
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Levels')

        # Call the circle button 
        self.circle_button = circle_button(50,50,50,color['button_color'],self.screen)
        
        pygame.mouse.set_visible(True) 

    def gameloop(self):
        run = True  
        while run:
            for event in pygame.event.get():
                mouse_x,mouse_y = pygame.mouse.get_pos() # get mouse position
                is_howered = self.circle_button.draw().collidepoint(mouse_x,mouse_y)
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: # mouse event 
                    if self.circle_button.draw().collidepoint(event.pos):
                        print("HIt It")
            pygame.mouse.set_cursor(*self.circle_button.hand_cursor) if is_howered else pygame.mouse.set_cursor(*self.circle_button.arrow_cursor)
            self.circle_button.color = color['hover_color'] if is_howered else color['button_color']
            self.circle_button.draw()
            pygame.display.update()    

class circle_button:
    def __init__(self, x, y, radius, color,screen):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.screen = screen

        self.setup_cursor()
    def setup_cursor(self):
        # Image load 
        hand_cursor = pygame.image.load('assets/hand_cursor.png')
        hand_cursor = pygame.transform.scale(hand_cursor, (20, 20))
        self.hand_cursor = pygame.cursors.Cursor((0, 0), hand_cursor)
        self.arrow_cursor = pygame.cursors.arrow

    def draw(self):
        font = pygame.font.SysFont('Comic Sans MS',20)
        text = font.render('Level 1', True, color['white'])

        cirlce = pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        self.screen.blit(text,(self.x-30,self.y-15))
        return cirlce

game = maingame()                
game.gameloop()