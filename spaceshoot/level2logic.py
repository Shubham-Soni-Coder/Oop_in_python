from gamelogic import gamebasic,spaceship,enemy,bullet,healtbar,color
import pygame 
import random
import sys


class Level2(gamebasic):
    def __init__(self, width=1200, height=800):
        self.spawn_next_enemy = True  # control one enemy spawn at a time
        super().__init__(width, height)
        self.width = 1200
        self.height = 800
        self.after_time = 1000 // 3 # faster the bullet spawn
        self.enemy_speed += 1 # increase the enemy speed
        self.required_score = 25 # increase the level score

    def spawn_enemy(self):
        self.enemy = enemy(self.height, self.width,self.screen,self.enemy_images,self.enemy_speed)
        self.enemyhealtbar = healtbar(self.enemy.enemy_x - 20, self.enemy.enemy_y,30, 5, 100,self.medkit_image)
        self.spawn_next_enemy = False

    def gameloop(self):
        self.run = True
        pygame.time.set_timer(self.my_event, self.after_time, loops=1)
        pygame.time.set_timer(self.medkit_event, random.randint(5000, 10000), loops=1)
        self.call_classes()
        self.spawn_enemy()
        while self.run:
            self.screen.fill(color['black'])
            if self.userhealtbar.current_hp <= 0:
                pygame.mouse.set_visible(True)
                self.after_gameover()

            if self.spaceship.score >= self.required_score:
                pygame.mouse.set_visible(True)
                self.levelup.play()
                self.after_win()

            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and self.spaceship.ship_y > 0:
                self.spaceship.move(0, -10)
            elif key[pygame.K_DOWN] and self.spaceship.ship_y < self.height - self.spaceship.ship_size:
                self.spaceship.move(0, 10)
            elif key[pygame.K_LEFT] and self.spaceship.ship_x > 0:
                self.spaceship.move(-10, 0)
            elif key[pygame.K_RIGHT] and self.spaceship.ship_x < self.width - self.spaceship.ship_size:
                self.spaceship.move(10, 0)

            for b in self.bullet_list[:]:
                b.update()
                if b.bullet_y < 0:
                    self.bullet_list.remove(b)
                if b.mask.overlap(self.enemy.enemy_mask,
                                  (self.enemy.enemy_x - b.bullet_x,
                                   self.enemy.enemy_y - b.bullet_y)):
                    try:
                        self.bullethit.play()
                        self.enemyhealtbar.current_hp -= 40
                        self.bullet_list.remove(b)
                    except Exception as e:
                        print(f'Error: {e}')
                
            if self.spaceship.ship_mash.overlap(self.enemy.enemy_mask,
                                                (self.enemy.enemy_x - self.spaceship.ship_x,
                                                 self.enemy.enemy_y - self.spaceship.ship_y)):
                self.hitsound.play()
                self.userhealtbar.current_hp -= 25
                self.enemyhealtbar.current_hp = self.enemyhealtbar.max_hp
                self.enemy.choice_image(reset=True)

            if self.enemy.enemy_y >= self.height:
                self.hitsound.play()
                self.userhealtbar.current_hp -= 25
                self.spawn_next_enemy = True

            if self.enemyhealtbar.current_hp <= 0:
                self.spaceship.score += 1
                self.spawn_next_enemy = True


            if self.spaceship.ship_mash.overlap(self.userhealtbar.medkit_mask,
                                                (self.medkit_x - self.spaceship.ship_x,
                                                 self.medkit_y - self.spaceship.ship_y)):
                if self.userhealtbar.current_hp < self.userhealtbar.max_hp:
                    self.medkit_effect.play()
                    self.userhealtbar.current_hp += 20
                    self.medkit_y = -25

            if self.medkit_show:
                self.userhealtbar.draw_medkit(self.screen, self.medkit_x, self.medkit_y)

            if self.show:
                fps_text = self.clock.get_fps()
                self.show_fps(fps_text)

            self.spaceship.import_image()
            self.spaceship.display_score(self.width)
            self.enemy.choice_image()
            self.userhealtbar.draw(self.screen)
            self.enemyhealtbar.update_value(self.enemy.enemy_x, self.enemy.enemy_y)
            self.enemyhealtbar.draw(self.screen)
            if self.spawn_next_enemy:
                self.spawn_enemy()

            self.simple_event()
            self.clock.tick(self.fps)
            pygame.display.flip()



maingame = Level2()
if __name__ == "__main__":
    maingame.gameloop()
