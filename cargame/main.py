import pygame
import random
import os 
import sys

pygame.init()
pygame.mixer.init()

class game:
    def __init__(self, width, height):
        # config window
        self.height, self.width = height, width 
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Cargame")

        # my car variable        
        self.car_x = self.height // 2 - 50
        self.car_y = self.width // 2 + 90

        # Gamestart
        self.gamestart = 0     

        # other car variable
        self.othercar_xs = [num for num in range(200, 900, 100)]
        self.othercar_x = 200
        self.othercar_y = -230  # Start off-screen

        pygame.key.set_repeat(500, 200)  # repeat key 

        self.gamescore = 0 
        self.highscore = 0

        # load sound
        try:
            self.starting_sound = pygame.mixer.Sound('start.mp3')
        except pygame.error as e:
            print(f"Failed to load sound effect: {e}")
            sys.exit()   

        # load images
        try:
            self.mycar_image = pygame.image.load('mycar.png')
            self.mycar_image = pygame.transform.scale(self.mycar_image, (100, 230))
            self.othercar_image = pygame.image.load('car1.png')
            self.othercar_image = pygame.transform.scale(self.othercar_image, (100, 230))
            self.start_image = pygame.image.load('start.png')
            self.start_image = pygame.transform.scale(self.start_image, (self.width, self.height))
            self.over_image = pygame.image.load('gameover.jpg')
            self.over_image = pygame.transform.scale(self.over_image, (self.width, self.height))
        except pygame.error as e:
            print(f"Failed to load image: {e}")
            sys.exit()

        # color: dic
        self.color = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 100, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
        }

    def Allscore(self):
        # create highscore file if not exist
        if not os.path.exists('highscore.txt'):
            with open('highscore.txt', 'w') as file:
                file.write('0')

        # open Highscore file
        with open('highscore.txt', 'r') as f:
            self.highscore = int(f.read())

        self.hifont = pygame.font.Font(None, 30)
        text = self.hifont.render(f'High Score: {self.highscore}', True, self.color['white'])
        self.screen.blit(text, (self.height + 60, 10))

        # Make score
        self.font = pygame.font.Font(None, 35)
        text = self.font.render(f'Score: {self.gamescore}', True, self.color['white'])
        self.screen.blit(text, (10, 10))

    def side_rect(self):
        self.siderect1 = self.height // 2 - 200  # Left rect coordinate
        self.siderect2 = self.height // 2 + 400  # right rect coordinate
        pygame.draw.rect(self.screen, self.color['green'], (0, 0, self.siderect1, self.width))  # Left rect
        pygame.draw.rect(self.screen, self.color['green'], (self.siderect2, 0, self.width, self.height))  # Right rect

    def background(self):
        self.sideline1_x = self.height // 2 - 200  # Left line coordinate
        self.sideline2_x = self.height // 2 + 400  # Right line coordinate
        self.centreline_x = self.height // 2 + 100  # Centre line coordinate
        self.sideline_y = self.width  # both line y 
        pygame.draw.line(self.screen, self.color['white'], (self.sideline1_x, 0), (self.sideline1_x, self.height), 10)  # Left line 
        pygame.draw.line(self.screen, self.color['white'], (self.sideline2_x, 0), (self.sideline2_x, self.height), 10)  # right line
        pygame.draw.line(self.screen, self.color['yellow'], (self.centreline_x, 0), (self.centreline_x, self.height), 10)  # Centre
        self.side_rect()  # Call rect function

    def car(self):
        # GENERATE MY CAR 
        self.mycar_rect = self.mycar_image.get_rect()  # save as rect
        self.mycar_rect.center = (self.car_x, self.car_y) 
        self.screen.blit(self.mycar_image, self.mycar_rect)  # update screen

        # GENERATE OTHER CAR       
        self.othercar_rect = self.othercar_image.get_rect()  # save as rect
        self.othercar_rect.center = (self.othercar_x, self.othercar_y)
        self.screen.blit(self.othercar_image, self.othercar_rect)  # update screen

    def main(self):
        self.firstscreen = True  # make a starting screen
        self.screen.blit(self.start_image, (0, 0))
        self.starting_sound.play()  # play the starting sound 
        pygame.display.update()

        while self.firstscreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.firstscreen = False
                    self.exitgame = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.firstscreen = False
                        self.gamestart = 50    
                        self.starting_sound.stop()
                        pygame.time.delay(500) 
                        self.gameloop()  # load the gameloop

    def overscreen(self):
        self.screen.blit(self.over_image, (0, 0))
        self.gameover = True 
        pygame.display.update()

        while self.gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameover = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        self.gameover = False
                        self.othercar_y = 0  # make othercar to y axis to 0  
                        self.gamescore = 0  # restart gamescore
                        self.othercar_x = 200  # restart x to othercar
                        self.gameloop()

    # check collision
    def collision(self): 
        if self.mycar_rect.colliderect(self.othercar_rect):
            self.exitgame = True

    def show_fps(self):
        fps = self.clock.get_fps()
        fps_font = pygame.font.Font(None, 30)
        fps_text = fps_font.render(f'FPS: {int(fps)}', True, self.color['white'])
        self.screen.blit(fps_text, (self.width - 150, 20)) 

    def gameloop(self):
        # gameloop variable
        self.exitgame = False 
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.gameover = False

        while not self.exitgame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exitgame = True
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.car_y > 100:
                        self.car_y -= 100
                    if event.key == pygame.K_DOWN and self.car_y < 600:
                        self.car_y  += 100
                    if event.key == pygame.K_LEFT and self.car_x > 200:
                        self.car_x  -= 100
                    if event.key == pygame.K_RIGHT and self.car_x < 700:
                        self.car_x  += 100
                    if event.key == pygame.K_SPACE:
                        self.gamestart = 20

            self.othercar_y += self.gamestart  # othercar movement speed

            # check for othercar out from screen
            if self.othercar_y > self.height + 100:
                self.gamescore += 1
                self.othercar_y = -230  # Reset to start off-screen
                self.othercar_x = random.choice(self.othercar_xs)

            # check for highscore 
            if self.gamescore > self.highscore:
                self.highscore = self.gamescore
                with open('highscore.txt', 'w') as f:
                    f.write(str(self.highscore))

            # Call All Functions
            self.screen.fill(self.color['black'])
            self.background()  # add background to game 
            self.car()  # generate car
            self.collision()  # check collision 
            self.Allscore()  # show high score
            self.show_fps()  # Show FPS on the screen

            self.clock.tick(self.fps)  # handle fps
            pygame.display.update()  # screen update 

        pygame.quit()
        sys.exit()

''' <-----               CLASS HAVE BE FINSHED                  -------->'''

Game = game(900, 700)
Game.main()

