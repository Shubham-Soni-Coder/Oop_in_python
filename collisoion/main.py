import pygame
import sys
import random
import os 

pygame.init()


class game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.window =  pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption('game') # set title 

        #circle variable
        self.circle_x = self.width // 2
        self.circle_y = self.height // 2
        self.radius = 20
        self.speed_x = 5
        self.speed_y = 5

        # fps variable
        self.fps = 120
        self.clock = pygame.time.Clock()

        # rect variable 
        self.line_start = 200  # start point
        self.line_end = self.height - 250  # end point 

        # time variable
        self.starting_time = pygame.time.get_ticks() #start time with 0 
        self.timer = 3 # countending point

        # color 
        self.color:dict = {
            'white':(255,255,255),
            'black':(0,0,0),
            'blue':(0,0,255),
            'green':(0,255,0),
            'red':(255,0,0),
            'yellow':(255,255,0)
        } 

        # game variable 
        self.exit = False
        self.start = 0
        self.random_start = random.choice([1,-1]) 
        self.score = 0
        self.highscore = 0 
        pygame.key.set_repeat(50) #repeat key 

        # music variable 
        self.hit = pygame.mixer.Sound('hit.wav')
        self.over_sound = pygame.mixer.Sound('gameover.wav')
        self.gamestart = pygame.mixer.Sound('gamestart.wav')

    def Allscore(self):
        # check for file
        if not os.path.exists('highscore.txt'):
            with open('highscore.txt','w') as file:
                file.write('0')

        with open('highscore.txt','r') as file: # if it open it
            self.highscore = int(file.read())

        # score
        score_font = pygame.font.Font(None,30)
        text = score_font.render(f"Score: {self.score}",True,self.color['white'])
        self.window.blit(text,(10,10))

        # highscore
        text = score_font.render(f"Highscore: {self.highscore}",True,self.color['white'])
        self.window.blit(text,(self.width-150,10))

    def createcircle(self): #create ball
        pygame.draw.circle(self.window, self.color['red'], (self.circle_x,self.circle_y), self.radius)

    def createrect(self): # create rect. of side
        # line1 
        pygame.draw.line(self.window,self.color['red'],(0,self.line_start),(0,self.line_end),5)

        # line2
        pygame.draw.line(self.window,self.color['red'],(self.width,self.line_start),(self.width,self.line_end),8)

    def after_gameover(self):
        self.gameover = True
        
        self.over_sound.play() # play sound when game over
        font = pygame.font.Font(None,75) # font of game over text
        game_over_text = font.render("Game Over",True,self.color['white'])
        self.window.blit(game_over_text,(self.width//2-120,self.height//2-50))
        
        score_text = font.render(f"Score: {self.score}",True,self.color['white'])
        self.window.blit(score_text,(self.width//2-120,self.height//2))
        
        pygame.display.update()
        while self.gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE,pygame.K_RETURN,pygame.K_KP_ENTER]:
                        self.__init__(self.width, self.height)
                        self.over_sound.stop()
                        self.gamestart.play()
                        self.gameover = False

    def mainloop(self): 
        while not self.exit:
            self.window.fill(self.color['black'])  

            elapsed_time = (pygame.time.get_ticks() - self.starting_time)//1000 # start time with 0 and add 1 it 
            current_time = self.timer - elapsed_time # check current time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP,pygame.K_w] and self.line_start > 0:
                        self.line_start -= 30  
                        self.line_end -= 30
                    if event.key in [pygame.K_DOWN,pygame.K_s] and self.line_end  <= self.height:
                        self.line_start += 30
                        self.line_end += 30

            if current_time >=0:    
                font = pygame.font.Font(None,75) # font of timer
                timer_text = font.render(f"Time left:{current_time}",True,self.color['white'])
                self.window.blit(timer_text,(self.width//2-120,self.height//2+250)) 

            else:
                self.start = self.random_start # random direction    

            # update ball position 
            self.circle_x += self.speed_x * self.start
            self.circle_y += self.speed_y * self.start 
            # check for collision 
            if (self.circle_x - self.radius <= 0 and self.line_start <= self.circle_y <= self.line_end) or \
            (self.circle_x + self.radius >= self.width and self.line_start <= self.circle_y<= self.line_end):
                self.speed_x = - self.speed_x
                self.score += 1  
                self.hit.play() # play sound when hit
            #  if collision is not found and left and right wall check 
            elif   self.circle_x - self.radius <= 0 or self.circle_x + self.radius >= self.width:
                self.after_gameover()
            # up and down wall check
            if self.circle_y - self.radius <= 0 or self.circle_y + self.radius >= self.height:
                self.speed_y= -self.speed_y # revsre the direction

            if self.score > self.highscore: 
                self.highscore = self.score

                with open('highscore.txt','w') as file:
                    file.write(str(self.highscore))
                
            # call function
            self.createcircle()
            self.createrect()
            self.Allscore()
            
            # update screen
            self.clock.tick(self.fps)
            pygame.display.update()

game = game(1000,600)
game.mainloop()