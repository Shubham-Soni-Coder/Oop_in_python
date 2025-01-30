import pygame
import random
import os 
import sys


pygame.init()

# define all color
color = {  
            'white': (255,255,255),
            'red': (255,0,0),
            'blue': (0,0,255),
            'green': (0,255,0),
            'black':(0,0,0)
        }

class gamebasic:
    def __init__(self,width=900,height=700):
        self.width = width
        self.height = height 
        self.screen =  pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption('spacegame') # set title

        # game varible
        self.run = False
        self.clock = pygame.time.Clock() 
        self.fps = 60 
        self.after_time = 1000 // 2 # set timer in milli seconds 
        self.show = False
        self.remaining_life = 5 
        # custem event 
        self.my_event = pygame.USEREVENT + 1 # event for 1 sec 
        # mouse variable 
        self.mouse_press = True

        # bullet management 
        self.bullet_list = []   

    def show_fps(self,fps_text):

        font = pygame.font.SysFont(None, 30)
        fps_surface = font.render(f'FPS: {int(fps_text)}', True, color['white'])
        self.screen.blit(fps_surface, (10, 20))

    def simple_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
                sys.exit()   
            elif event.type == self.my_event: # check for my event 
                self.bullet_list.append(
                    bullet(self.screen,self.spaceship.ship_x+57,self.spaceship.ship_y-12)
                )     
                pygame.time.set_timer(self.my_event,self.after_time,loops=1) # make new one in 0.5       
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL: # event of mouse visible or not 
                    self.mouse_press = not self.mouse_press
                    pygame.mouse.set_visible(self.mouse_press)
                if event.key==pygame.K_SPACE:
                    self.show = not self.show

    def call_classes(self):
        self.spaceship = spaceship(self.height//2,self.width//2, self.screen) # Call the spaceship class
        self.enemy = enemy(self.height,self.width,self.screen) # call the enemy class
        self.bullet = bullet(self.screen,self.spaceship.ship_x+57,self.spaceship.ship_y-12) # call the bullet class
        self.userhealtbar = healtbar(0,0,100,20,100) # user spaceship healt bar 
        self.enemyhealtbar = healtbar(self.enemy.enemy_x-20,self.enemy.enemy_y,30,5,100) # class of enemy healtbar

    def after_gameover(self):
        self.run = False
        font = pygame.font.SysFont(None, 60)
        textsurface = font.render('Game Over', True, color['white'])
        self.screen.blit(textsurface, (self.width//2-100, self.height//2))
        pygame.display.update()
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_KP_ENTER,pygame.KSCAN_KP_ENTER]:
                        game_over = False
                        self.run = True
                        # self.spaceship.reset()
                        # self.enemy.reset()
                        self.gameloop()



    def gameloop(self): 
        self.run = True
        pygame.time.set_timer(self.my_event,self.after_time,loops=1) # start the timer 
        self.call_classes() # call all the classes 
        while self.run:
            self.screen.fill(color['black']) # set background color to black
            if self.userhealtbar.current_hp <= 0:
                self.after_gameover() # game over
            
            if self.spaceship.remaining_life <= 0 :
                self.after_gameover() 

            # get key presss     
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.spaceship.ship_y > 0 :
                self.spaceship.move(0,-10)
            elif key[pygame.K_DOWN]and self.spaceship.ship_y < self.height- self.spaceship.ship_size:
                self.spaceship.move(0,10)
            elif key[pygame.K_LEFT] and self.spaceship.ship_x>0:
                self.spaceship.move(-10,0)
            elif key[pygame.K_RIGHT] and self.spaceship.ship_x<self.width - self.spaceship.ship_size:
                self.spaceship.move(10,0)  
            # update and draw bullet 
            for b in self.bullet_list[:]:
                b.update()
                if b.bullet_y < 0 : # check if the ball is out from the screen
                    self.bullet_list.remove(b)

            # check for collision between user spaceship bullet and enemy spaceship
                if b.mask.overlap(self.enemy.enemy_mask,
                                  (self.enemy.enemy_x - b.bullet_x,
                                   self.enemy.enemy_y - b.bullet_y)):
                    try:
                        self.enemyhealtbar.current_hp -= 25 * 2
                        self.bullet_list.remove(b) 
                    except Exception as e:
                        print(f'Error: {e}')

            # check for collision between user spaceship and enemy spaceship
            if self.spaceship.ship_mash.overlap(self.enemy.enemy_mask,
                                                (self.enemy.enemy_x - self.spaceship.ship_x,
                                                 self.enemy.enemy_y - self.spaceship.ship_y)):
                self.userhealtbar.current_hp -= 25
                self.enemyhealtbar.current_hp = self.enemyhealtbar.max_hp # reset enemyhealtbar 
                # Create a new enemy spaceship at a random position
                self.enemy.choice_image(reset=True)  
            if self.enemy.enemy_y>= self.height: # enemy ship out from screen
                self.enemyhealtbar.current_hp = 100
                self.spaceship.remaining_life -= 1 
            if self.enemyhealtbar.current_hp <= 0: # if 0
                self.spaceship.score += 1 
                self.enemy.choice_image(reset=True) # create a new enemy spaceship 
                self.enemyhealtbar.current_hp = self.enemyhealtbar.max_hp # reset healtbar
            
            # show fps
            if self.show:
                fps_text = self.clock.get_fps()
                self.show_fps(fps_text)
            self.spaceship.import_image() # create image of spaceship
            self.spaceship.display_score(self.width) 
            self.spaceship.display_remain_life(self.width)
            self.enemy.choice_image() # random image choices
            self.userhealtbar.draw(self.screen) 
            self.enemyhealtbar.update_value(self.enemy.enemy_x,self.enemy.enemy_y)
            self.enemyhealtbar.draw(self.screen)
            self.simple_event() 
            self.clock.tick(self.fps)
            pygame.display.flip()


class healtbar():
    def __init__(self,x,y,w,h,max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.current_hp = max_hp  # set the current hp to max_hp 
        self.max_hp = max_hp

    def update_value(self,x,y): # update the x and y coodinte in main loop
        self.x = x 
        self.y = y

    def draw(self,screen):
        ratio = self.current_hp/self.max_hp
        pygame.draw.rect(screen,color['red'],(self.x,self.y,self.w,self.h)) # full hp rect 
        pygame.draw.rect(screen,color['green'],(self.x,self.y,self.w*ratio,self.h)) # current hp rect

class spaceship():
    def __init__(self,ship_x, ship_y,screen):
        self.ship_x = ship_x
        self.ship_y = ship_y 
        self.remaining_life = 5 
        self.ship_size = 150 # use in further
        self.screen = screen  
        self.score = 0
        #import image 
        self.ship = pygame.image.load('assests/ship.png').convert_alpha()
        self.ship_mash = pygame.mask.from_surface(self.ship)
            
    def move(self,dx,dy):
        self.ship_x+= dx    
        self.ship_y+= dy
        self.import_image()

    def import_image(self):
        self.ship_position = self.ship_x , self.ship_y 
        self.screen.blit(self.ship,self.ship_position)

    def display_score(self,width):
        self.print_score = pygame.font.SysFont(None,30)
        self.score_surface = self.print_score.render(f"Score:{int(self.score)}",True,color['white'])
        self.screen.blit(self.score_surface,(width-80,10))

    def display_remain_life(self,width):
        self.show_remain_life = pygame.font.SysFont(None,30)
        self.remain_life_surface = self.show_remain_life.render(f"Life:{self.remaining_life}",True,color['white'])
        self.screen.blit(self.remain_life_surface,(width-68,30))

        if self.remaining_life <= 0:
            print('gameover')



class bullet():
    def __init__(self,screen,bullet_x,bullet_y):
        self.bullet_x = bullet_x
        self.bullet_y = bullet_y
        self.bullet_list  = []
        self.screen = screen
        self.image = pygame.image.load('assests/bullet.png')
        self.image = pygame.transform.scale(self.image,(20,20))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.image_pos = (self.bullet_x,self.bullet_y)
        self.screen.blit(self.image,self.image_pos)
        self.bullet_y -= 5 

class enemy:
    def __init__(self,height,width,screen):
        self.height = height
        self.width = width
        self.screen = screen
    
        self.enemy_list  = [
            pygame.transform.scale(pygame.image.load(f'assests/enemy{i}.png').convert_alpha(),(100,100))
            for i in range(3)
        ]

        self.get_image = random.choice(self.enemy_list) # choice the image reandom
        self.enemy_x = random.randint(0,self.width-100) # x random
        self.enemy_y = -self.get_image.get_height() - 20  # start the enemy y to - point        
        self.choice_image()
    
    def choice_image(self,reset=False):
        if self.enemy_y > 700 or reset: 
            self.get_image = random.choice(self.enemy_list)
            self.enemy_x = random.randint(0,self.width-100)
            self.enemy_y = -self.get_image.get_height() - 20
             

        self.position = (self.enemy_x,self.enemy_y) 
        self.enemy_mask = pygame.mask.from_surface(self.get_image)
        self.screen.blit(self.get_image,self.position)
        self.enemy_y += 3




game = gamebasic()
game.gameloop()
