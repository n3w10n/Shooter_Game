x = 1000
y = 50
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
from pygame import *
from random import randint

window_width = 700
window_height = 500
window = display.set_mode((window_width, window_height))
display.set_caption("Catch")

bg = transform.scale(image.load("background.jpg"), (window_width, window_height))

class Character():
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed):
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

class Wall(Character):
    def __init__(self, size_x, size_y, pos_x, pos_y):
        self.size_x = size_x
        self.size_y = size_y
        self.image = Surface( (size_x, size_y))
        self.image.fill( (252, 3, 44))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

player1 = Character("hero.png", 50, 50, 50, 450, 5)
player2 = Character("cyborg.png", 75, 75, 150, 200, 5)
player3 = Character("treasure.png",100, 100, 600, 0, 2)

wall_list = []

wall_list.append(Wall(20, 100 , 120, 400))
wall_list.append(Wall(20, 400, 5, 0))
wall_list.append(Wall(170, 20, 120, 280))
wall_list.append(Wall(170, 20, 120, 100))
wall_list.append(Wall(20, 200, 120, 100))
wall_list.append(Wall(20, 100, 580, 0))
wall_list.append(Wall(170, 20, 120, 400))
wall_list.append(Wall(20, 100 , 270, 400))
wall_list.append(Wall(20, 300, 410, 100))
wall_list.append(Wall(190, 20, 410, 100))
wall_list.append(Wall(150, 20, 410, 400))
wall_list.append(Wall(150, 20, 550, 250))
# wall_list.append(Wall())

game = True
finish = False

clock = time.Clock()
fps = 60
route = 0

route_list = [(625, 200), (625, 305), (120, 305), (120, 20), (300, 20), (300, 305), (430, 305), (430, 20), (625, 20)]
# route_list = []

# for i in range(10):
#     x = randint(25, window_width - 25)
#     y = randint(25, window_height - 25)
#     route_list.append((x, y))

ok_x = False
ok_y = False

font.init()
style = font.SysFont(None, 70)
style2 = font.SysFont(None, 30)
isWin = True 


player1.hp = 3
while game:
    window.blit(bg, (0, 0))
    player1.draw()
    player2.draw()
    player3.draw()
    for w in wall_list:
        w.draw()
    text = style2.render("HP = " + str(player1.hp), 1, (144, 179, 30))
    window.blit(text, (20, 0))
        
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish == False:
        safety_x = player1.rect.x
        safety_y = player1.rect.y
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and player1.rect.x < window_width-player1.size_x:
            player1.rect.x += player1.speed
        elif keys_pressed[K_LEFT] and player1.rect.x > 0:
            player1.rect.x -= player1.speed
        elif keys_pressed[K_UP] and player1.rect.y> 0 :
            player1.rect.y -= player1.speed
        elif keys_pressed[K_DOWN] and player1.rect.y < window_height-player1.size_y :
            player1.rect.y += player1.speed

        for w in wall_list:
            if sprite.collide_rect(player1, w):
                player1.rect.x = safety_x
                player1.rect.y = safety_y

        goto_x, goto_y = route_list[route]
        if player2.rect.x == goto_x:
            ok_x = True
        else:
            dist = abs(goto_x - player2.rect.x)
            if player2.rect.x < goto_x:
                player2.rect.x += min(player2.speed, dist)
            elif player2.rect.x > goto_x:
                player2.rect.x -= min(player2.speed, dist)

        if player2.rect.y == goto_y:
            ok_y = True
        else:
            dist = abs(goto_y - player2.rect.y)
            if player2.rect.y < goto_y:
                player2.rect.y += min(player2.speed, dist)
            elif player2.rect.y > goto_y:
                player2.rect.y -= min(player2.speed, dist)


        if ok_x and ok_y:
            player2.speed = randint(5, 20)
            route += 1
            ok_x = False
            ok_y = False
            if route == len(route_list):
                route = 0

        if sprite.collide_rect(player1, player2):
            
            player1.hp -= 1
            player1.rect.x = 50
            player1.rect.y = 450
            
            if player1.hp == 0:
                finish = True
                isWin = False
                print("YOU LOSE")
        elif sprite.collide_rect(player1, player3):
                finish = True
                isWin = True
                print("YOU WIN")
    else:
        if isWin == True:
            text = style.render("YOU WIN", 1, (58, 179, 30))
            window.blit(text, (200,300))
        if isWin == False:
            text = style.render("YOU LOSE", 1, (179, 30, 30))
            window.blit(text, (200,300))
    



    display.update()
    clock.tick(fps)