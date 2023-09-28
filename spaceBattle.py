# Alexandr Zhelanov, https://soundcloud.com/alexandr-zhelanov

import pygame, sys
import random
import math
import os

WIDTH = 1200
HEIGHT = 720
FPS = 60
# define colors ============================================================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# initialize pygame and create window========================================
pygame.init()
pygame.font.init()
pygame.mixer.init() # khoi tao sound effect 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()
font_name = pygame.font.match_font('arial')

def drawText(S, text, size, x, y, COLOR):
    font = pygame.font.Font(font_name, size)
    text_S = font.render(text, True, COLOR)
    text_rect = text_S.get_rect()
    text_rect.midtop = (x,y)
    S.blit(text_S, text_rect)

def eventListener():
    for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

def gotoScreenHome():
    screen.blit(bg, (0,0))
    drawText(screen, "WELCOME!", 35, WIDTH/2, 20, GREEN)   
    drawText(screen, "Press SPACE to play", 28, WIDTH/2, 60, GREEN)   
    drawText(screen, "Use A,D,S,W to move left/right or up/down", 28, WIDTH/2, HEIGHT/3, WHITE)   
    drawText(screen, "Move your mouse and press left click to shoot the meteor", 28, WIDTH/2, HEIGHT/3 + 50, WHITE)  
    drawText(screen, "Press 1/2 to change gun", 28, WIDTH/2, HEIGHT/3 + 100, WHITE)  
    drawText(screen, "Press SPACE while in game to open SHOP", 28, WIDTH/2, HEIGHT/3 + 150, WHITE)   
    drawText(screen, "Click Right mouse to use Super Laser when your power is over 40", 28, WIDTH/2, HEIGHT/3 + 200, WHITE)   
    drawText(screen, "If you die, your bullet -2", 28, WIDTH/2, HEIGHT/3 + 250, WHITE)   
    drawText(screen, "Pick up Shield or Power to increase your shield or power", 28, WIDTH/2, HEIGHT/3 + 300, WHITE)   
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

def goShop():
    waiting = True
    while waiting:
        rect_screen = screen.get_rect()
        boxShop = pygame.Surface((600, 200))
        rect_boxShop = boxShop.get_rect()
        rect_boxShop.center = rect_screen.center
        x,y ,w, h = rect_boxShop
        pygame.draw.rect(screen, (200,200,200), (x,y,w,h), border_radius=20) # draw box shop
        pygame.draw.rect(screen, (150,150,150), (rect_screen.centerx-100, 100, 200,50), border_radius=20) #draw box coin
        drawText(screen, "Coins:", 30, rect_screen.centerx-50, 110, YELLOW)
        drawText(screen, str(player.coin)+"$", 30, rect_screen.centerx+40, 110, YELLOW)
        drawText(screen, "Shield - ", 30, x+50, rect_boxShop.top, BLUE)
        drawText(screen, "Lives - ", 30, x+50, rect_boxShop.centery-20, BLUE)
        drawText(screen, "Bullet - ", 30, x+50, rect_boxShop.bottom-40, BLUE)
        drawText(screen, "1k$ = 10Shield", 23, rect_boxShop.centerx+180, rect_boxShop.top, BLUE)
        drawText(screen, "20k$ = 1live", 23, rect_boxShop.centerx+180, rect_boxShop.centery-20, BLUE)
        drawText(screen, "5k$ = 1Bullet", 23, rect_boxShop.centerx+180, rect_boxShop.bottom-40, BLUE)
        drawShieldBar(screen, x+100, rect_boxShop.top, player.shield, w-300, 40)
        draw_lives(screen, x+100, rect_boxShop.centery-20, player.lives, mini_player_img)
        draw_bullet(screen, x+100, rect_boxShop.bottom-50, player.num_bullet, mini_bullet_img)
        drawButtonBuy(screen, rect_boxShop.right-50, rect_boxShop.top, miniBuy_img)
        drawButtonBuy(screen, rect_boxShop.right-50, rect_boxShop.centery-20, miniBuy_img)
        drawButtonBuy(screen, rect_boxShop.right-50, rect_boxShop.bottom-40, miniBuy_img)
        pygame.display.update()
        clock.tick(FPS)

        rectBuy1 = get_rect(miniBuy_img, rect_boxShop.right-50, rect_boxShop.top)
        rectBuy2 = get_rect(miniBuy_img, rect_boxShop.right-50, rect_boxShop.centery-20)
        rectBuy3 = get_rect(miniBuy_img, rect_boxShop.right-50, rect_boxShop.bottom-40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:         
                    if rectBuy1.collidepoint(pygame.mouse.get_pos()):
                        if player.shield < 100 and player.coin >= 1000:
                            player.shield += 10
                            player.coin -= 1000
                            if player.shield > 100:
                                player.shield = 100
                    if rectBuy2.collidepoint(pygame.mouse.get_pos()):
                        if player.lives < 5 and player.coin >= 20000:
                            player.lives += 1
                            player.coin -= 20000
                    if rectBuy3.collidepoint(pygame.mouse.get_pos()):
                        if player.num_bullet < 9 and player.coin >= 5000:
                            player.num_bullet += 1
                            player.coin -= 5000
def get_rect(img, x, y):
    rect_img = img.get_rect()
    rect_img.x = x
    rect_img.y = y
    return rect_img

def newmob(anim, speed):
    m = Mob(anim, speed)
    all_sprites.add(m)
    mobs.add(m)

def drawShieldBar(surf, x, y, pct, w, h):
    if pct < 0:
        pct = 0
    BAR_WIDTH = w
    BAR_HEIGHT = h
    fill = (pct/100) * BAR_WIDTH
    outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 60:
        colorBar = (37,186,203)
    elif 30 <= pct <= 60:
        colorBar = YELLOW
    elif pct < 30:
        colorBar = RED
    pygame.draw.rect(surf, colorBar, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y 
        surf.blit(img, img_rect)

def drawButtonBuy(surf, x, y, img):
    img_rect = img.get_rect()
    img_rect.x = x
    img_rect.y = y
    surf.blit(img, img_rect)

def draw_bullet(surf, x, y, bullet, img):
    for i in range(bullet):
        img_rect = img.get_rect()
        img_rect.x = x + 20 * i
        img_rect.y = y 
        surf.blit(img, img_rect)

def bonusCoins(last_time):
    while True:
        now = pygame.time.get_ticks()
        drawText(screen, "Your score achieved 2000 and rewarded 1000 coins", 30, WIDTH/2, HEIGHT/2, BLUE)
        pygame.display.update()
        if now - last_time > 1500:
            break

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (30,40))
        self.image.set_colorkey(BLACK) # loai bo mau den trong image
        # self.image = pygame.S((50, 80))
        # self.image.fill(GREEN)w
        self.rect = self.image.get_rect()
        self.radius = 25
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 2)
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT - 100
        self.speedx = 8
        self.speedy = 8
        self.orig_image = self.image.copy() # Store a reference to the original.
        self.bullet_type = 0
        self.shield = 100
        self.power = 0
        self.num_bullet = 1
        self.num_bullet_time = pygame.time.get_ticks()
        self.bullet_type = 0
        self.damge = 1
        self.shoot_delay = 200

        self.last_shoot = pygame.time.get_ticks()
        self.lives = 2
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.coin = 1000

    def update(self):
        # if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 5000: # thoi gian su dung power 5s
        #     self.power -= 1
        #     self.power_time = pygame.time.get_ticks()

        if self.bullet_type == 0:
            self.damge = 1
            self.shoot_delay = 400
        elif self.bullet_type == 1:
            self.damge = 0.5
            self.shoot_delay = 250
        else :
            self.damge = 3
            self.shoot_delay = 1000

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1500:
            self.hidden = False
            self.rect.center = (WIDTH/2, HEIGHT - 100)

        if self.hidden == False:
            if self.rect.right > WIDTH: # kiem tra neu vuot qua gioi han display
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left =  0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            self.rotate()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            self.pos_mouse = pygame.mouse.get_pos()
            posMouse_x = self.pos_mouse[0]
            posMouse_y = self.pos_mouse[1]
            if self.num_bullet == 1:
                bullet = Bullet(self.rect.centerx, self.rect.centery, self.pos_mouse, self.angle, self.bullet_type)
                all_sprites.add(bullet)
                bullets.add(bullet)
            if self.num_bullet > 1:
                for i in range(1, self.num_bullet+1): 
                    if i%2 == 0:
                        posMouse_x = self.pos_mouse[0] + i*10
                        posMouse_y = self.pos_mouse[1] + i*10
                    else:
                        posMouse_x = self.pos_mouse[0] - i*10 - 10
                        posMouse_y = self.pos_mouse[1] - i*10 - 10
                    bullet = Bullet(self.rect.centerx, self.rect.centery, (posMouse_x, posMouse_y), self.angle, self.bullet_type)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
            laserSnd_ls[self.bullet_type].play()

    def beam(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > 1000:
            self.last_shoot = now
            if self.power >= 40:
                self.power -= 40
                self.pos_mouse = pygame.mouse.get_pos()
                bullet = Bullet(self.rect.centerx, self.rect.centery, self.pos_mouse, self.angle, 2)
                all_sprites.add(bullet)
                bullets.add(bullet)
                laserSnd_ls[self.bullet_type].play()

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        self.angle = math.degrees(math.atan2(-dy, dx)) - 90
        print(dx, dy)
        # Rotate the image by the negative angle (y-axis in pygame is flipped).
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)

    def num_bulletup(self):
        self.num_bullet += 1
        if self.num_bullet > 8:
            self.num_bullet = 8
        self.num_bullet_time = pygame.time.get_ticks()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 200)


class Mob(pygame.sprite.Sprite):
    def __init__(self, animat, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = animat[random.randrange(0, len(animat))]
        self.rScale = random.randrange(1, 5)
        self.x = 20; self.y = 20
        self.radius = 13*self.rScale # badt buoc phai co self.radius thi moi su dung duoc pygame.sprites.circle
        self.image = pygame.transform.scale(self.image,(self.x*self.rScale, self.y*self.rScale)) # thay doi kich thuoc meteor
        self.image_orig = self.image.copy() # ban san cua image goc
        self.rect = self.image.get_rect()
        self.hp = 1*self.rScale
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius, 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = speed
        self.speedy = random.randrange(1, 6)*self.speed
        self.speedx = random.randrange(-2, 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8,10)
        self.lastUpdate = pygame.time.get_ticks()  # thoi diem bat dau
        self.frame = 0

    def rotate(self):
        now = pygame.time.get_ticks() # thoi diem hien tai
        if now - self.lastUpdate > 50:
            self.lastUpdate = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot)
            self.rect = self.image.get_rect(center=self.rect.center)

    def animationMeteors(self):
        now = pygame.time.get_ticks() # thoi diem hien tai
        if now - self.lastUpdate > 1000:
            self.frame += 1
            if self.frame == len(meteor_anim):
                self.frame = 0
            center = self.rect.center
            self.image = meteor_anim[self.frame]
            self.image = pygame.transform.scale(self.image,(self.x*self.rScale, self.y*self.rScale))
            self.rect = self.image.get_rect()
            self.rect.center = center

    def update(self):
        self.rotate()
        # self.animationMeteors()
        self.rect.x += self.speedx
        self.rect.y += self.speedy 
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.kill()
            newmob(all_meteor[name_meteor][0], self.speed)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, cx, cy, pos_mouse, angle_rotate, bullet_type):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_type = bullet_type
        if bullet_type == 2:
            self.image = pygame.image.load(os.path.join(bullet_dir, bullet_list[bullet_type])).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50,900))
        else:
            self.image = pygame.image.load(os.path.join(bullet_dir, bullet_list[bullet_type]))
            
        self.rect = self.image.get_rect()
        self.rect.centerx = cx
        self.rect.centery = cy
        self.speed = 15
        self.last_time_beam = pygame.time.get_ticks()

        mouse_x = pos_mouse[0]
        mouse_y = pos_mouse[1]
        distance_x = mouse_x - self.rect.centerx
        distance_y = mouse_y - self.rect.centery
        angle = math.atan2(distance_y, distance_x) # caculate bullet move
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

        self.orig_image = self.image # Store a reference to the original.
        self.image = pygame.transform.rotate(self.orig_image, angle_rotate) # rotate bullet to mouse
        self.rect = self.image.get_rect(center=self.rect.center)
    def update(self):
        self.rect.x = int(self.rect.x + self.dx)
        self.rect.y = int(self.rect.y + self.dy)
        if self.bullet_type != 2:
            # kill if it moves off the top of the screen
            if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH:
                self.kill()
        if self.bullet_type == 2:
            if pygame.time.get_ticks() - self.last_time_beam > 2000:
                self.kill()
            

class Explosion(pygame.sprite.Sprite):
    def __init__(self, rectMob, name):
        pygame.sprite.Sprite.__init__(self)
        self.xMob, self.yMob, self.wMod, self.hMod = rectMob
        self.name = name
        self.image = exp_anim[self.name][0]
        if self.name == "mob":
            self.image = pygame.transform.scale(self.image, (self.wMod, self.hMod))
        elif self.name == "player":
            self.image = pygame.transform.scale(self.image, (self.wMod*4, self.hMod*4))
        self.rect = self.image.get_rect()
        self.rect.center = (self.xMob + self.wMod/2, self.yMob + self.hMod/2)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 40 # toc do explosion effect

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(exp_anim[self.name]):
                self.kill()
            else:
                center = self.rect.center
                self.image = exp_anim[self.name][self.frame]
                if self.name == 'mob':
                    self.image = pygame.transform.scale(self.image, (self.wMod, self.hMod))
                elif self.name == "player":
                    self.image = pygame.transform.scale(self.image, (self.wMod+50, self.hMod+50))
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_img[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill it if moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, center, coin_value):
        pygame.sprite.Sprite.__init__(self)
        self.image = coin_anim[0]
        self.image = pygame.transform.scale(self.image, (20,20))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3
        self.last_time = pygame.time.get_ticks()
        self.frame = 0
        self.coin_value = coin_value - 10

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_time > 150:
            self.last_time = now
            self.frame += 1
            if self.frame == len(coin_anim):
                self.frame = 0   
            self.image = coin_anim[self.frame]
            self.image = pygame.transform.scale(self.image, (20,20))
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center
        self.rect.y += self.speedy
        # kill it if moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

def loadAnimation(list, dir, animArray):
    for anim in list:
        file = os.path.join(dir, anim)
        image = pygame.image.load(file).convert_alpha()
        image.set_colorkey(BLACK)
        animArray.append(image)

# Load all imgs ==========================================================================
img_dir = os.path.join(os.path.dirname(__file__), 'img')
bullet_dir = os.path.join(img_dir, 'bullet')
exp_anim_dir = os.path.join(img_dir, 'Explosions_kenney')
player_dir = os.path.join(img_dir,"DurrrSpaceShip.png")
coin_dir = os.path.join(img_dir,"Coin")
miniBuy_dir = os.path.join(img_dir,"Up.png")
meteor_dir = os.path.join(img_dir, 'asteroids/meteor')
asteroid1_dir = os.path.join(img_dir,"asteroids/1")
asteroid2_dir = os.path.join(img_dir,"asteroids/2")
asteroid3_dir = os.path.join(img_dir,"asteroids/3")

bg = pygame.image.load(os.path.join(img_dir, "spacefield_a-000.png")).convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
player_img = pygame.image.load(player_dir).convert()
mini_player_img = pygame.transform.scale(player_img, (20, 30))
mini_player_img.set_colorkey(BLACK)
miniBuy_img = pygame.image.load(miniBuy_dir).convert()
miniBuy_img = pygame.transform.scale(miniBuy_img, (40,40))
miniBuy_img.set_colorkey(BLACK)

bullet_list = os.listdir(bullet_dir)
mini_bullet_img = pygame.image.load(os.path.join(bullet_dir, bullet_list[0]))
mini_bullet_img = pygame.transform.scale(mini_bullet_img ,(50,50))
meteor_list = os.listdir(meteor_dir)
exp_anim_list = os.listdir(exp_anim_dir)
coin_anim_list = os.listdir(coin_dir)
asteroid1_list = os.listdir(asteroid1_dir)
asteroid2_list = os.listdir(asteroid2_dir)
asteroid3_list = os.listdir(asteroid3_dir)

asteroid1_anim = []
loadAnimation(asteroid1_list, asteroid1_dir, asteroid1_anim)
asteroid2_anim = []
loadAnimation(asteroid2_list, asteroid2_dir, asteroid2_anim)
asteroid3_anim = []
loadAnimation(asteroid3_list, asteroid3_dir, asteroid3_anim)
meteor_anim = []
loadAnimation(meteor_list, meteor_dir, meteor_anim)

all_meteor = {}
all_meteor['meteor'] = []
all_meteor['asteroid1'] = []
all_meteor['asteroid2'] = []
all_meteor['asteroid3'] = []
all_meteor['meteor'].append(meteor_anim)
all_meteor['asteroid1'].append(asteroid1_anim)
all_meteor['asteroid2'].append(asteroid2_anim)
all_meteor['asteroid3'].append(asteroid3_anim)

list_wave = ['meteor', 'asteroid1', 'asteroid2', 'asteroid3']
name_meteor = random.choice(list_wave)

exp_anim = {}
exp_anim['mob'] = []
exp_anim['player'] = []
loadAnimation(exp_anim_list, exp_anim_dir, exp_anim['mob'])
loadAnimation(exp_anim_list, exp_anim_dir, exp_anim['player'])

coin_anim = []
loadAnimation(coin_anim_list, coin_dir, coin_anim)

powerup_img = {}
powerup_img['gun'] = pygame.image.load(os.path.join(img_dir, 'bolt_gold.png')).convert()
powerup_img['shield'] = pygame.image.load(os.path.join(img_dir, 'shield_gold.png')).convert()

# Load all sounds ===================================================================
sound_dir = os.path.join(os.path.dirname(__file__), 'sound')
laserSnd_ls = []
for snd in ["Laser_Shoot2.wav", 'Laser_Shoot3.wav', 'Laser_Shoot.wav']:
    laserSnd_ls.append(pygame.mixer.Sound(os.path.join(sound_dir, snd)))

expSnd_ls = []
for snd in ['Explosion1.wav', 'Explosion2.wav']:
    expSnd_ls.append(pygame.mixer.Sound(os.path.join(sound_dir, snd)))

player_die_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'Die_Sound.wav'))
pygame.mixer.music.load(os.path.join(sound_dir,'Space Atmosphere.mp3'))
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(loops=-1)

# Game loop
gameOver = True
running = True
playerCoin = 0
while running:
    clock.tick(FPS)
    if gameOver == True:
        gotoScreenHome()
        gameOver = False
        # init sprites, players, mobs
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        num_bullets = pygame.sprite.Group()
        coins = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        speed = 1
        for i in range(8):
            newmob(all_meteor[name_meteor][0], speed)
        last_time_level = pygame.time.get_ticks()
        time_delay_wave = pygame.time.get_ticks()
        score = 0
        wait_wave = False
        num_meteor = 1
        level_wave = 1

    if score >= 2000:
        player.coin += 1000
        score = 0
        last_time_bonusCoin = pygame.time.get_ticks()
        bonusCoins(last_time_bonusCoin)

    now_time_level = pygame.time.get_ticks()
    # kiem tra thoi gian cua 1 wave
    if now_time_level - last_time_level > 60000 and wait_wave == False:
        wait_wave = True
        num_meteor += 0.5
        level_wave += 1
        speed += 0.2
        last_time_level = now_time_level
        time_delay_wave = now_time_level
        for mob in mobs:
            mob.kill()
    # thoi gian cho wave moi
    if now_time_level - time_delay_wave > 5000 and wait_wave == True:
        last_time_level = now_time_level
        time_delay_wave = now_time_level
        wait_wave = False
        name_meteor = random.choice(list_wave)
        for i in range(1, int(6*num_meteor)):
            newmob(all_meteor[name_meteor][0], speed)

    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.bullet_type = 0
            if event.key == pygame.K_2:
                player.bullet_type = 1
            if event.key == pygame.K_SPACE:
                goShop()
    # player move
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        player.rect.x -= player.speedx
    if key[pygame.K_d]:
        player.rect.x += player.speedx
    if key[pygame.K_w]:
        player.rect.y -= player.speedy
    if key[pygame.K_s]:
        player.rect.y += player.speedy
    
    # player shoot
    mouse_press = pygame.mouse.get_pressed()
    if mouse_press[0]: # left click
        player.shoot()
    if mouse_press[2]: # right click
        player.beam()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, False, False)
    mobHits = hits.keys()
    bulletHits = hits.values()
    hit = len(bulletHits)
    if hits:
        player.power += 1
    if player.power >= 100:
        player.power = 100
    for b in bulletHits:
        bullet = b[0]
        damge = player.damge
    for mob in mobHits:
        mob.hp -= (hit * damge)
        if mob.hp <= 0:
            random.choice(expSnd_ls).play()
            score += mob.radius
            exp = Explosion(mob.rect, 'mob')
            all_sprites.add(exp)
            newmob(all_meteor[name_meteor][0], mob.speed)
            mob.kill()
            if random.random() > 0.95:
                pow = Power(mob.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            if random.random() > 0.4:
                coin = Coin(mob.rect.center, mob.radius)
                all_sprites.add(coin)
                coins.add(coin)
        if bullet.bullet_type != 2:
            bullet.kill()

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) # bat buoc moi sprite phai co self.radius thi moi su dung duoc ham collide_circle
    for hit in hits:
        player.shield -= hit.radius
        exp = Explosion(hit.rect, 'mob')
        all_sprites.add(exp)
        newmob(all_meteor[name_meteor][0], hit.speed)
        random.choice(expSnd_ls).play()
        if player.shield <= 0:
            death_expl = Explosion(player.rect, 'player')
            all_sprites.add(death_expl)
            player.lives -= 1
            player.shield = 100
            player.hide()
            player_die_sound.play()
            player.num_bullet -= 2
            if player.num_bullet < 1:
                player.num_bullet = 1

    # check to see if the player hit the power
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            # player.num_bulletup()
            player.power += 25
            if player.power >= 100:
                player.power = 100

    # check to see if the player hit the coin
    hits = pygame.sprite.spritecollide(player, coins, True)
    for hit in hits:
        player.coin += hit.coin_value
        
    if player.lives == 0:
        # running = False
        gameOver = True

    # Update
    all_sprites.update()

    # Draw / render
    screen.blit(bg, (0,0))
    all_sprites.draw(screen)   
    drawText(screen,"Score: "+str(score), 28, WIDTH-100, 60, WHITE)
    drawText(screen, "Coin: " + str(player.coin), 28, (WIDTH - 100), 100, YELLOW)
    drawText(screen,"Time: "+str(int((now_time_level - last_time_level)/1000)), 20, (WIDTH/2), 10, WHITE)
    drawText(screen,"Your need to survival 60s", 20, (WIDTH/2), 30, WHITE)
    drawText(screen,"Wave: "+str(level_wave), 20, (WIDTH/2), 50, WHITE)
    drawShieldBar(screen, 5, 5, player.shield, WIDTH/6, 20)
    drawShieldBar(screen, 5, 30, player.power, WIDTH/6, 20) # power bar
    draw_lives(screen, WIDTH - 150, 10, player.lives, mini_player_img)
    if wait_wave == True:
        drawText(screen, "Good job! You're still alive", 30, WIDTH/2, HEIGHT/2 - 30, WHITE)
        drawText(screen, "Next wave will come in "+str(5-int((now_time_level-time_delay_wave)/1000))+"s", 30, WIDTH/2, HEIGHT/2, WHITE)
        
    # *after* drawing everything, flip the display
    pygame.display.flip()
pygame.quit()
sys.exit()