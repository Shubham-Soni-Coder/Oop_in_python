import pygame
import random
import os 
import sys


pygame.init()
pygame.mixer.init()


class game:
    def __init__(self,width,height):
        
        # config window
        self.height,self.width = height,width 
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Cargame")

        # my car variable        
        self.car_x = self.height//2-50
        self.car_y = self.width//2+90

        # Gamestart
        self.gamestart = 0     

        # other car variable
        self.othercar_xs:list = [num for num in range(200,700,100)]
        self.othercar_x = 200
        self.othercar_y = self.width//2-380

        pygame.key.set_repeat(500,200) # repeat key 

        self.gamescore = 0 
        self.highscore = 0

        # load sound
        try:
           self.starting_sound = pygame.mixer.Sound('start.mp3')
        except pygame.error as e:
            print(f"Failed to load sound effect: {e}")
            sys.exit()   


        # color: dic
        self.color = {
            'white':(255,255,255),
            'black':(0,0,0),
            'red':(255,0,0),
            'green':(0,100,0),
            'blue':(0,0,255),
            'yellow':(255,255,0),
        }


        
    def Allscore(self):
        # create highscore file if not exist
        if (not os.path.exists('highscore.txt')):
            with open('highscore.txt', 'w') as file:
                file.write('0')

         # open Highscore file
        with open('highscore.txt','r') as f:
            self.highscore = int(f.read())

        
        self.hifont = pygame.font.Font(None, 30)
        text = self.hifont.render(f'High Score: {self.highscore}', True, self.color['white'])
        self.screen.blit(text,(self.height+60,10))

        # Make score
        self.font = pygame.font.Font(None, 35)
        text = self.font.render(f'Score: {self.gamescore}', True, self.color['white'])
        self.screen.blit(text, (10, 10))
        pygame.display.update()    



    def side_rect(self):
        self.siderect1 = self.height//2-200 # Left rect coodinte
        self.siderect2 = self.height//2+400 # right rect coodinte
        pygame.draw.rect(self.screen,self.color['green'],(0,0,self.siderect1,self.width)) # Left rect
        pygame.draw.rect(self.screen, self.color['green'], (self.siderect2,0, self.width, self.height)) # Right rect

    def background(self):
        self.sideline1_x = self.height//2-200 #Left line coodinte
        self.sideline2_x = self.height//2+400 #Right line coodinte
        self.centreline_x = self.height//2+100 #Centre line coodinte
        self.sideline_y = self.width  # both line y 
        pygame.draw.line(self.screen, self.color['white'], (self.sideline1_x, 0), (self.sideline1_x, self.height), 10) #Left line 
        pygame.draw.line(self.screen, self.color['white'], (self.sideline2_x, 0), (self.sideline2_x, self.height), 10) #right line
        pygame.draw.line(self.screen, self.color['yellow'], (self.centreline_x, 0), (self.centreline_x, self.height), 10) #Centre
        self.side_rect() # Call rect function

    def car(self):
        try:
            # GENERTE MY CAR 
            self.mycar = pygame.image.load('mycar.png') # load mycar image
            self.mycar = pygame.transform.scale(self.mycar,(100,230)) # into 100,230 
            self.mycar_rect = self.mycar.get_rect() # save as rect
            self.mycar_rect.center = (self.car_x,self.car_y) 
            self.screen.blit(self.mycar,self.mycar_rect) # update screen

            # GENERTE OTHER CAR       
            self.othercar = pygame.image.load('car1.png') #load othercar image
            self.othercar = pygame.transform.scale(self.othercar,(100,230)) # into 100,230
            self.othercar_rect = self.othercar.get_rect() # save as rect
            self.othercar_rect.center = (self.othercar_x,self.othercar_y)
            self.screen.blit(self.othercar,self.othercar_rect) #update screen
        except pygame.error as e:
            print(f"Failed to load image: {e}")
            sys.exit()    
   

    def main(self):
        self.firstscreen = True #make a starting screen
        # load image 
        try:
            self.image = pygame.image.load('start.png')
            self.image = pygame.transform.scale(self.image,(self.width,self.height))
            self.screen.blit(self.image,(0,0))

            self.starting_sound.play() # play the starting sound 
            
            pygame.display.update() 
        except pygame.error as e:
            print(f"Failed to load image: {e}")
            sys.exit()    

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
                        self.gameloop() # load the gameloop

    def overscreen(self):
        try:
            self.overimage = pygame.image.load('gameover.jpg') # load overgame screen 
            self.overimage = pygame.transform.scale(self.overimage,(self.width,self.height))
            self.screen.blit(self.overimage,(0,0))
            self.gameover = True 
            pygame.display.update()
        except pygame.error as e:
            print(f"Failed to load image: {e}")
            sys.exit()    
        while self.gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameover = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN,pygame.K_KP_ENTER]:
                        self.gameover = False #
                        self.othercar_y = 0 # make othercar to y asix to 0  
                        self.gamescore = 0  # restert gamescore
                        self.othercar_x = 200 # restert x to othercar
                        self.gameloop()
                        
    # check collision
    def collision(self): 
        if self.mycar_rect.colliderect(self.othercar_rect):
            self.exitgame = True


    def gameloop(self):
        # gameloop variable
        self.exitgame = False 
        self.clock = pygame.time.Clock()
        self.fps = 120
        self.gameover = False
        # start game
        
        while not self.exitgame :
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
                    if event.key==pygame.K_SPACE:
                        self.gamestart = 80     
   
            self.othercar_y +=self.gamestart #othercar movement speed


        
            # check for othercar out from screen
            if self.othercar_y > self.height:
                self.gamescore += 1 # 
                self.othercar_y = self.width//2-380 #start to one 
                self.othercar_x = random.choice(self.othercar_xs) # choce x 

            # check for highscore 
            if self.gamescore > self.highscore:
                self.highscore = self.gamescore # 
                with open('highscore.txt','w') as f:
                    f.write(str(self.highscore))
            
            self.clock.tick(self.fps) # handle fps
            
            

            # Call ALl FUNCTION
            self.screen.fill(self.color['black'])
            self.background() # add background to game 
            self.car() # gentrate car
            self.collision() # check collision 
            self.Allscore() # show high score
            

            if self.exitgame:
                self.overscreen() # show over screen when game over

            pygame.display.update()  # screen update 
        pygame.quit()
        sys.exit()
    


''' <-----               CLASS HAVE BE FINSHED                                -------->'''

Game = game(900,700)
Game.main()

