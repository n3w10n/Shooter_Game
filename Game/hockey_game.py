x = 100
y = 50
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
from pygame import *
from random import randint, choice
import time as timer

window_width = 1600
window_height = 800
window = display.set_mode((window_width, window_height))
display.set_caption("Air Hockey")

bg = transform.scale(image.load("air_hockey_stadium.jpg"), (window_width, window_height))

class Character(sprite.Sprite):
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed):
        sprite.Sprite.__init__(self)
        self.filename = filename
        self.size_x = size_x
        self.size_y = size_y
        self.image = transform.scale(image.load(filename), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.speed = speed
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Ball(Character):
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed):
        super().__init__(filename, size_x, size_y, pos_x, pos_y, speed)
        self.speed_x = speed
        self.speed_y = speed
        self.angle = 0
        self.rotate_speed = 3
        self.rotate_image = self.image
        self.rotate_rect = self.rotate_image.get_rect()
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x < 0 or self.rect.x > window_width-75:
            self.speed_x *= -1
        if self.rect.y < 0 or self.rect.y > window_height-75:
            self.speed_y *= -1
    def rotate(self):
        self.angle += self.rotate_speed
        self.rotate_image = transform.rotate(self.image, self.angle)
        self.rotate_rect = self.rotate_image.get_rect(center = (self.rect.x, self.rect.y))
    def draw(self):
        window.blit(self.rotate_image, (self.rotate_rect.x, self.rotate_rect.y))




player1 = Character("air_hockey_striker.png", 100, 100, 100, 352, 8)
player1.score = 0
player2 = Character("air_hockey_striker.png", 100, 100, 1400, 352, 8)
player2.score = 0
puck = Ball("plane.png", 75, 75, 760, 365, 10)

game = True
finish = False

font.init()
style = font.SysFont(None, 100)

start_restart = timer.time()

clock = time.Clock()
fps = 60

isDelay = False
while game:
    window.blit(bg, (0, 0))

    player1.draw()
    player2.draw()
    puck.draw()
    
    text = style.render(str(player1.score) + " " + "VS" + " " + str (player2.score), 1, (144, 179, 30))
    window.blit(text, (700, 0))

    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish == False:
        
        if isDelay == False:
            puck.rotate()
            puck.update()
            keys_pressed = key.get_pressed()
            if keys_pressed[K_s] and player2.rect.y < window_height-player1.size_y:
                player1.rect.y += player1.speed
            if keys_pressed[K_w] and player1.rect.y > 0:
                player1.rect.y -= player1.speed
            if keys_pressed[K_UP] and player2.rect.y> 0 :
                player2.rect.y -= player2.speed
            if keys_pressed[K_DOWN] and player2.rect.y < window_height-player2.size_y :
                player2.rect.y += player2.speed

            if sprite.collide_rect(player1, puck):
                puck.speed_x = abs(puck.speed_x)
            
            if sprite.collide_rect(player2, puck):
                puck.speed_x = -abs(puck.speed_x)

            if (puck.rect.x < 0):
                player2.score += 1
                puck.rect.x = 760
                puck.rect.y = 365
                isDelay = True
                start_restart = timer.time()
            if (puck.rect.x > window_width-75):
                player1.score += 1
                puck.rect.x = 760
                puck.rect.y = 365
                isDelay = True
                start_restart = timer.time()

            if player1.score >= 5 or player2.score >= 5:
                finish = True

            

        elif timer.time() - start_restart > 2:
            isDelay = False
    else:

        if player1.score >= 5:
            text_result = style.render("PLAYER 1 WINS", 1, (144, 179, 30))
        if player2.score >= 5:
            text_result = style.render("PLAYER 1 WINS", 1, (144, 179, 30))
        window.blit(text_result, (700, 400))

    display.update()
    clock.tick(fps)