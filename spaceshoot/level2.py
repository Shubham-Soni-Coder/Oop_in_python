import pygame
from level1 import GameStart
from level2logic import maingame


# Initalize pygame only once 
pygame.init()
class logic(GameStart):
    def __init__(self,width=maingame.width,height=maingame.height):
        super().__init__(width, height)
        self.required_score = maingame.required_score
        self.start = maingame

        #call all function 
        self.setup_fonts()
        self.setup_cursors()
        self.setup_texts()
        self.setup_button()


    def main_loop(self):
        return super().main_loop()


main = logic()

if __name__=="__main__":
    main.main_loop()
