import pygame 
import sys

pygame.init()

screen = pygame.display.set_mode((600,700))

ship_y = 700
ship_x = 200

ship = pygame.image.load('assests/ship.png')

clock = pygame.time.Clock()

run = True
while run:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()
    screen.blit(ship,(ship_x,ship_y))
    clock.tick(60)
    ship_y -= 10

    if ship_y < 0:
        print_line = pygame.font.SysFont(False,40)
        text = print_line.render('You Win',True,'Green')
        screen.blit(text,(700/2,600/2))
    pygame.display.update()




