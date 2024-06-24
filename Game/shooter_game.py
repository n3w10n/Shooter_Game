x = 1000
y = 50
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
from pygame import *
from random import randint, choice
import time as timer

window_width = 700
window_height = 800
window = display.set_mode((window_width, window_height))
display.set_caption("Catch")

bg = transform.scale(image.load("galaxy.jpg"), (window_width, window_height))

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
class UFO(Character):
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed, hp, isRespawn):
        super().__init__(filename, size_x, size_y, pos_x, pos_y, speed)
        self.max_hp = hp
        self.hp = hp
        self.isRespawn = isRespawn
    
    def update(self):
        global pass_count
        self.rect.y += self.speed
        if self.rect.y > 900:
            self.rect.y = 0
            self.rect.x = randint(50, 650)
            self.speed = randint(2, 15)
            pass_count += 1

    def shot(self):
        global shot_count
        self.hp -= 1
        if self.hp == 0:
            print("UFO is destroyed")
            shot_count += 1
            if self.isRespawn == True:
                self.respawn()
            else:
                self.kill()
    
    def respawn(self):
        self.rect.y = 0
        self.rect.x = randint(0, 650)
        self.speed = randint(2, 8)
        self.hp = self.max_hp
    
class Bullet(Character):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(Character):
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed):
        super().__init__(filename, size_x, size_y, pos_x, pos_y, speed)
        self.speed_x = choice([4, 3, 2, -2, -3, -4])
        self.speed_y = choice([4, 3, 2, -2, -3, -4])
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x < 0 or self.rect.x > window_width or self.rect.y < 0 or self.rect.y > window_height:
            self.kill()
            print("Killed the asteroid")
    

player1 = Character("rocket.png", 50, 50, 350, 750, 7)

ufo_group = sprite.Group()
ufo_group.add( UFO("ufo.png", 100, 75, 150, 200, 5, 2, True) )
ufo_group.add( UFO("ufo.png", 100, 75, 150, 0, 5, 2, True) )

Asteroid_group = sprite.Group()
Asteroid_group.add( Asteroid("asteroid.png", 100, 100, randint(200, window_width-200), randint(200, window_height-200), 0))
next_aesteroid_time = randint(2,4)
last_aesteroid_time = timer.time()

bullet_group = sprite.Group()

game = True
finish = False

clock = time.Clock()
fps = 60

font.init()
style = font.SysFont(None, 70)
style2 = font.SysFont(None, 30)
isWin = True 


font.init()
style = font.SysFont(None, 36)
pass_count = 0
last_fire_time = timer.time()

magazine = 30
bullets_remain = magazine
isReload = False
allowReload = True
shot_count = 0
start_reload_time = timer.time()
boss_count = 0
style = font.SysFont(None, 36)

hp = 5
style = font.SysFont(None, 36)

blink_count = 0

isBossEvent = True

while game:
    window.blit(bg, (0, 0))
    player1.draw()
    Asteroid_group.draw(window)
    ufo_group.draw( window )
    bullet_group.draw(window)
        
    text = style.render("Missed:" + str(pass_count), 1, (255, 255, 255))
    window.blit(text, (20, 20))

    mag = style.render("Magazine:" + str(bullets_remain), 1, (255, 255, 255))
    window.blit(mag, (20, 40))

    health = style.render("Health:" + str(hp), 1, (255, 255, 255))
    window.blit(health, (20, 60))

    kills = style.render("Kills:" + str(shot_count), 1, (255, 255, 255))
    window.blit(kills, (20, 80))

    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish == False:
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and player1.rect.x < window_width-player1.size_x:
            player1.rect.x += player1.speed
        if keys_pressed[K_LEFT] and player1.rect.x > 0:
            player1.rect.x -= player1.speed
        if keys_pressed[K_UP] and player1.rect.y> 0 :
            player1.rect.y -= player1.speed
        if keys_pressed[K_DOWN] and player1.rect.y < window_height-player1.size_y :
            player1.rect.y += player1.speed
        if keys_pressed[K_SPACE] and timer.time() - last_fire_time >  0.2 and bullets_remain > 0 and allowReload == True:
            bullet_group.add(Bullet("bullet.png", 20, 40, player1.rect.x, player1.rect.y, 5))
            bullets_remain -= 1
            last_fire_time = timer.time()
        if keys_pressed[K_r] and isReload == False:
            isReload = True
            allowReload = False
            start_reload_time = timer.time()
        if(isReload == True):
            if blink_count < 20:
                mag = style.render(("Reloading..."), 1, (255, 255, 255))
            elif blink_count < 40:
                mag = style.render((" "), 1, (255, 255, 255))
            elif blink_count < 60:
                mag = style.render((" "), 1, (255, 255, 255))
                blink_count = 0
            window.blit(mag, (300, 440))
            blink_count += 1
            if (timer.time() - start_reload_time > 2):
                bullets_remain = magazine
                isReload = False
                allowReload = True

        collide_list = sprite.spritecollide(player1, ufo_group, False)
        for collided_ufo in collide_list:
            if collided_ufo.isRespawn == True:
                x = randint(100, window_width - 100)
                ufo_group.add(UFO("ufo.png", 100, 75, x , 0, 5, 2, True) )
                hp -= 1
            else:
                hp -= 3
            collided_ufo.kill()
        
        if hp <= 0:
            finish = True
        

        collide_dict =  sprite.groupcollide(bullet_group, ufo_group, True, False)
        for bullet_key in collide_dict:
            ufo = collide_dict[bullet_key][0]
            ufo.shot()

        if shot_count % 5 == 0 and shot_count != 0:
            if isBossEvent == True:
                ufo_group.add( UFO("ufo.png", 300, 150, 200, 0, 2, 10, False))
                isBossEvent = False
        else:
            isBossEvent = True

        if timer.time() - last_aesteroid_time > next_aesteroid_time :
            Asteroid_group.add( Asteroid("asteroid.png", 100, 100, randint(200, window_width-200), randint(200, window_height-200), 0))
            last_aesteroid_time = timer.time()

        collide_list = sprite.spritecollide(player1, Asteroid_group, True)
        if len(collide_list):
            hp -= 1

        collide_dict = sprite.groupcollide(Asteroid_group, ufo_group, True, False)
        for asteroid_key in collide_dict:
            ufo = collide_dict[asteroid_key][0]
            ufo.respawn()

        ufo_group.update()
        bullet_group.update()
        if shot_count >= 10:
            finish = True
    else:
        if shot_count >= 10:
            text_result = style.render("YOU WIN", 1, (255,255,255))
        else:
            text_result = style.render("YOU LOSE", 1, (255, 255, 255))
        window.blit(text_result, (300, 440))

        
    Asteroid_group.update()
    display.update()
    clock.tick(fps)