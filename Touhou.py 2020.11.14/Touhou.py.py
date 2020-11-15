# Touhou.py
# Created by Alpha_Stream

import pygame

import random

import time

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_w,
    K_a,
    K_s,
    K_d,
    QUIT
)

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 800


try: 
    with open("internals/highscore.txt", "r") as file_object:
        prevHIGHSCORE = int(file_object.read())
        #print(prevHIGHSCORE)
except FileNotFoundError:
    print("\nMissing game files. Please reinstall")
    time.sleep(3)
    exit()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("assets/image/reimu.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (40,57))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect = self.surf.get_rect(center=(250,750))

    def update(self, pressed_keys):
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -1)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, 1)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-1, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(1, 0)

        if self.rect.left < 28:
            self.rect.left = 28
        elif self.rect.right > 500:
            self.rect.right = 500
        if self.rect.top <= 28:
            self.rect.top = 28
        elif self.rect.bottom >= 772:
            self.rect.bottom = 772


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("assets/image/bullet.png").convert_alpha()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(random.randint(38, 490), 38))
        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom >= 762:
            self.kill()

class PointCollector(pygame.sprite.Sprite):
    def __init__(self):
        super(Collection, self).__init__()
        self.surf = pygame.image.load("assets/image/blank hitbox.png").convert_alpha()
        self.rect = self.surf.get_rect((28,771))

def collision(self, sprite):
    return self.rect.colliderect(sprite.rect)

def main():
    print("Loading game...")
    pygame.init()
    pygame.display.set_caption("Touhou.py")
    icon = pygame.image.load("assets/image/icon.png")
    pygame.display.set_icon(icon)
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    time.sleep(10) #########
    
    hitsound = pygame.mixer.Sound("assets/audio/hitsound.wav")

    bgm = ["assets/audio/songs/night of nights.mp3", "assets/audio/songs/lunatic eyes invisible full moon.mp3", "assets/audio/songs/voyage 1970.mp3"]
    selectedBGM = random.choice(bgm)
    pygame.mixer.init()
    pygame.mixer.music.load(selectedBGM)
    pygame.mixer.music.set_volume(0.04)
    pygame.mixer.music.play()

    if selectedBGM == "assets/audio/songs/night of nights.mp3":
        background = "assets/image/themes/wind god's lake.png"
    elif selectedBGM == "assets/audio/songs/lunatic eyes invisible full moon.mp3":
        background = "assets/image/themes/skies of gensokyo.png"
    elif selectedBGM == "assets/audio/songs/voyage 1970.mp3":
        background = "assets/image/themes/mysterious cherry blossom path.png"

    bg = pygame.image.load(background).convert_alpha()
    
    FPSfont = pygame.font.SysFont("Arial", 27)
    clock = pygame.time.Clock()

    COMBOfont = pygame.font.SysFont("Arial", 48)

    SCOREfont = pygame.font.SysFont("Arial", 48)
    
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 100)

    player = Player()

    enemies = pygame.sprite.Group()
    collector = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    PointCollector.containers = collector, all

    global score

    SCORE = 0
    COMBO = 0
    LIVES = 1
    newHIGHSCORE = False
    
    print("Game loaded successfully!")
    startTime = time.time()
    
    running = True
    
    while running:
        thisTime = time.time()
        #screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
        SCORE = int(time.time() - startTime)
        realSCORE = str(SCORE * int((SCORE/10)+1))
        COMBO = str(int((SCORE/10)))
        screen.blit(bg, (0,0))
        score = SCOREfont.render(str(int(realSCORE)), True, pygame.Color("white"))
        screen.blit(score, (810, 105))
        combo = COMBOfont.render(str(int(COMBO)), True, pygame.Color("white"))
        screen.blit(combo, (810, 184))
        fps = FPSfont.render(str(int(clock.get_fps())), True, pygame.Color("white"))
        screen.blit(fps, (798, 762))
        clock.tick(10000)
                                
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        
        if pygame.sprite.spritecollideany(player, enemies):
            pygame.mixer.Channel(0).play(hitsound, maxtime = 2000)
            enemies.empty()
            #enemies.draw(screen)
            LIVES = LIVES - 1
            screen.blit(bg, (0,0))
            screen.blit(bg, (0,0))

            
            if LIVES == 0:
                pygame.mixer.Channel(0).play(hitsound, maxtime = 2000)
                
                running = False
                state = True
                time.sleep(1)
                player.kill()
                pygame.quit()
                if prevHIGHSCORE < int(realSCORE):
                    newHIGHSCORE = True
                else:
                    newHIGHSCORE = False
                
                print("\n\n             RESULTS")
                print("Score        " + str(realSCORE))
                #print("OG Score     " + str(SCORE))
                print("Combo        " + str(COMBO))
                if newHIGHSCORE == True:
                    print("NEW HIGHSCORE!")
                    with open("internals/highscore.txt", "w") as file_object:
                        file_object.write(realSCORE)
                    newHIGHSCORE = False
                        
                    
                while state == True:
                    #print("Time (sec)   " + str(time.time() - startTime))
                    theInput = input("\nRetry? y/n >> ")
                    if theInput == "y":
                        main()
                        pygame.quit()
                        state = False
                    elif theInput == "n":
                        print("Quitting game...")
                        exit()
                        state = False
                    elif theInput == "reset":
                        print("Resetting highscore...")
                        with open("internals/highscore.txt", "w") as file_object:
                            file_object.write("0")
                        print("Highscore has been reset successfully. Please restart the game.")
                        time.sleep(3)
                        exit() 
                    else:
                        print("Invalid input.")
                        state = True            


        pygame.display.flip()

print("\n\n")
print("Touhou.py")
print("")
print("Instructions: use arrow keys (up,down,left,right) to dodge the blue bullets.")
print("\nGame will start in 3 seconds...")     
time.sleep(3)
main()
