import pygame
import random
import os 
import sys

pygame.mixer.pre_init(44100,-16,2,512)  
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
    def __init__(self,width=1200,height=700):
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
        # custem event 
        self.my_event = pygame.USEREVENT + 1 # event for bullet  
        self.medkit_show = False
        self.medkit_event = pygame.USEREVENT + 2 
        # mouse variable 
        self.mouse_visible = False
        pygame.mouse.set_visible(self.mouse_visible)
        # bullet management 
        self.bullet_list = []   
        # medkit variable 
        self.medkit_x = random.randint(20,self.width-50)
        self.medkit_y = random.randint(20,self.height)
        # music album
        try:
            self.bulletsound = pygame.mixer.Sound('assets/bulletfire.wav')
            self.bullethit = pygame.mixer.Sound('assets/bullethit.mp3')
            self.medkit_effect = pygame.mixer.Sound('assets/medkit_effect.mp3')
            self.levelup = pygame.mixer.Sound('assets/levelup.mp3')
            self.gameover_effect = pygame.mixer.Sound('assets/gameover.mp3')
            self.gamestart = pygame.mixer.Sound('assets/gamestart.wav')
            self.gameloop_sound = pygame.mixer.Sound('assets/gameloop.mp3')
            self.hitsound = pygame.mixer.Sound('assets/hitsound.mp3')
        except Exception as e:
            print(f"Failed to load sound effect:{e}")
            sys.exit()
    def show_fps(self,fps_text):
        font = pygame.font.SysFont(None, 30)
        fps_surface = font.render(f'FPS: {int(fps_text)}', True, color['white'])
        self.screen.blit(fps_surface, (10, 20))
    
    def nextlevel_button(self):
        # Button setup
        self.button_rect = pygame.Rect(self.width//2 - 100, self.height//2 + 100, 200, 60)
        font = pygame.font.Font(None, 36)
        button_text = font.render("Next Level", True, color['white'])

        # mouse 
        hand_mouse = pygame.SYSTEM_CURSOR_HAND
        arrow_mouse = pygame.SYSTEM_CURSOR_ARROW

        pygame.mouse.set_cursor(hand_mouse) if self.button_rect.collidepoint(pygame.mouse.get_pos()) else pygame.mouse.set_cursor(arrow_mouse)

        pygame.draw.rect(self.screen, color['blue'], self.button_rect, border_radius=10)
        self.screen.blit(button_text, (self.button_rect.x + 40, self.button_rect.y + 20))

    def simple_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                pygame.quit()
                sys.exit()   
            elif event.type == self.my_event: # check for my event
                self.bulletsound.play() # play bullet sound 
                self.bullet_list.append(
                    bullet(self.screen,self.spaceship.ship_x+57,self.spaceship.ship_y-12)
                    )     
                pygame.time.set_timer(self.my_event,self.after_time,loops=1) # make new one in 0.5       
            elif event.type == self.medkit_event: # check for medkit event 
                self.medkit_show = not self.medkit_show
                self.medkit_x = random.randint(20,self.width-50)
                self.medkit_y = random.randint(20,self.height)
                pygame.time.set_timer(self.medkit_event,random.randint(5000,10000),loops=1) # make new one in 7 seconds
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL: # event of mouse visible or not 
                   self.mouse_visible = not self.mouse_visible
                   pygame.mouse.set_visible(self.mouse_visible)
                if event.key==pygame.K_SPACE: # event for show fps 
                    self.show = not self.show
    def call_classes(self):
        self.spaceship = spaceship(self.height//2,self.width//2, self.screen) # Call the spaceship class
        self.enemy = enemy(self.height,self.width,self.screen) # call the enemy class
        self.bullet = bullet(self.screen,self.spaceship.ship_x+57,self.spaceship.ship_y-12) # call the bullet class
        self.userhealtbar = healtbar(0,0,100,20,100) # user spaceship healt bar 
        self.enemyhealtbar = healtbar(self.enemy.enemy_x-20,self.enemy.enemy_y,30,5,100) # class of enemy healtbar

    def after_gameover(self):
        # iamge of gameover
        self.gameover = pygame.image.load('assets/gameover.jpg')
        self.gameover = pygame.transform.scale(self.gameover,(self.width,self.height))
        
        self.gameover_effect.play()
        self.run = False
        font = pygame.font.SysFont(None, 40)
        textsurface = font.render(f'Score:{self.spaceship.score}', True, color['white'])
        self.screen.blit(self.gameover,(0,0))
        self.screen.blit(textsurface, (self.width//2-55, self.height-100))
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
                        self.gameover_effect.stop()
                        self.gamestart.play()               
                        pygame.mouse.set_visible(self.mouse_visible)
                        self.gameloop()
    def after_win(self):
        self.run = False
        self.levelup.play()
        ship = self.spaceship.ship
        ship_x = self.spaceship.ship_x
        ship_y = self.spaceship.ship_y  
        text = pygame.font.SysFont('Lucida Handwriting', 50)
        text_show = text.render("Congratulation", True, color['green'])
        text_show2 = text.render("You won this level!", True, color['green'])  # New line added
        win = True
        while win:
            self.screen.fill(color['black'])  # set background color to black
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    win = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(pos):
                        print('Next level starting...')
                    elif self.back_button_rect.collidepoint(pos):  # New line added
                        print('Going back to main menu...')  # New line added
                        win = False  # New line added
            self.screen.blit(ship, (ship_x, ship_y)) 
            self.clock.tick(self.fps)
            ship_y -= 10
            if ship_y < -20:
                text_rect = text_show.get_rect(center=(self.width / 2, self.height / 2))
                text_rect2 = text_show2.get_rect(center=(self.width / 2, self.height / 2 + 60))  # New line added
                self.screen.blit(text_show, text_rect)
                self.screen.blit(text_show2, text_rect2)  # New line added
                self.nextlevel_button()
                self.back_button()  # New line added
            pygame.display.update()

    def back_button(self):  # New method added
        self.back_button_rect = pygame.Rect(self.width//2 - 100, self.height//2 + 200, 200, 60)
        font = pygame.font.Font(None, 36)
        button_text = font.render("Back", True, color['white'])

        # mouse 
        hand_mouse = pygame.SYSTEM_CURSOR_HAND
        arrow_mouse = pygame.SYSTEM_CURSOR_ARROW

        pygame.mouse.set_cursor(hand_mouse) if self.back_button_rect.collidepoint(pygame.mouse.get_pos()) else pygame.mouse.set_cursor(arrow_mouse)

        pygame.draw.rect(self.screen, color['red'], self.back_button_rect, border_radius=10)
        self.screen.blit(button_text, (self.back_button_rect.x + 70, self.back_button_rect.y + 20))

    def gameloop(self): 
        self.run = True
        pygame.time.set_timer(self.my_event,self.after_time,loops=1)# timer for bullet
        pygame.time.set_timer(self.medkit_event,random.randint(5000,10000),loops=1)# timer for medkit 
        self.call_classes() # call all the classes 
        while self.run:
            self.screen.fill(color['black']) # set background color to black
            if self.userhealtbar.current_hp <= 0:
                pygame.mouse.set_visible(True)
                self.after_gameover() # game over
        
            if self.spaceship.score == 15:
                pygame.mouse.set_visible(True) # change visiblily of mouse
                self.after_win() # win the game

            # Keys event      
            key = pygame.key.get_pressed() # key pressed 
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
                        self.bullethit.play()
                        self.enemyhealtbar.current_hp -= 40
                        self.bullet_list.remove(b) 
                    except Exception as e:
                        print(f'Error: {e}')

            # check for collision between user spaceship and enemy spaceship
            if self.spaceship.ship_mash.overlap(self.enemy.enemy_mask,
                                                (self.enemy.enemy_x - self.spaceship.ship_x,
                                                 self.enemy.enemy_y - self.spaceship.ship_y)):
                self.hitsound.play()
                self.userhealtbar.current_hp -= 20
                self.enemyhealtbar.current_hp = self.enemyhealtbar.max_hp # reset enemyhealtbar 
                self.enemy.choice_image(reset=True)  # create enemy spaceship at random position 
            if self.enemy.enemy_y>= self.height: # enemy ship out from screen
                self.hitsound.play()
                self.enemyhealtbar.current_hp = 100
                self.userhealtbar.current_hp -= 20 

            if self.enemyhealtbar.current_hp <= 0:
                self.spaceship.score += 1 
                self.enemy.choice_image(reset=True) # create a new enemy spaceship 
                self.enemyhealtbar.current_hp = self.enemyhealtbar.max_hp # reset healtbar
            
            # check  collision between user spaceship and medkit 
            if self.spaceship.ship_mash.overlap(self.userhealtbar.medkit_mask,
                                                (self.medkit_x - self.spaceship.ship_x,
                                                self.medkit_y - self.spaceship.ship_y)):
                if self.userhealtbar.current_hp  < self.userhealtbar.max_hp:
                    self.medkit_effect.play()
                    self.userhealtbar.current_hp +=20
                    self.medkit_y = -50
            if self.medkit_show: 
                self.userhealtbar.draw_medkit(self.screen,self.medkit_x,self.medkit_y)
            # show fps
            if self.show:
                fps_text = self.clock.get_fps()
                self.show_fps(fps_text)
         
            self.spaceship.import_image() # create image of spaceship
            self.spaceship.display_score(self.width) 
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

        self.medkit = pygame.image.load('assets/medkit.png').convert_alpha()
        self.medkit = pygame.transform.scale(self.medkit,(50,50))
        self.medkit_mask = pygame.mask.from_surface(self.medkit)

    def update_value(self,x,y): # update the x and y coodinte in main loop
        self.x = x 
        self.y = y

    def draw(self,screen):
        ratio = self.current_hp/self.max_hp
        pygame.draw.rect(screen,color['red'],(self.x,self.y,self.w,self.h)) # full hp rect 
        pygame.draw.rect(screen,color['green'],(self.x,self.y,self.w*ratio,self.h)) # current hp rect

    def draw_medkit(self,screen,medkit_x,medkit_y):
        screen.blit(self.medkit,(medkit_x,medkit_y))
        medkit_y+= 10 
class spaceship():
    def __init__(self,ship_x, ship_y,screen):
        self.ship_x = ship_x
        self.ship_y = ship_y 
        self.ship_size = 150 # use in further
        self.screen = screen  
        self.score = 0
        #import image 
        self.ship = pygame.image.load('assets/ship.png').convert_alpha()
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

class bullet():
    def __init__(self,screen,bullet_x,bullet_y):
        self.bullet_x = bullet_x
        self.bullet_y = bullet_y
        self.bullet_list  = []
        self.screen = screen
        self.image = pygame.image.load('assets/bullet.png')
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
            pygame.transform.scale(pygame.image.load(f'assets/enemy{i}.png').convert_alpha(),(100,100))
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

maingame = gamebasic()

if __name__=="__main__":
    maingame.gameloop()
