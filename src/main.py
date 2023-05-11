import pygame
from pygame import mixer
from pygame.locals import *
import random
import sys
import os
pygame.init()
pygame.mixer.init()

###### Flappy Bird take 2 ########
### Using OOP ######
######## This is player version ###########

#### CONSTANT setup for screen display :#####
WIDTH = 864
HEIGHT = 936
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
LOGO = pygame.image.load(os.path.join("assets", "Flappy_Logo.png"))
pygame.display.set_icon(LOGO)
pygame.display.set_caption("FLAPPY BIRD DEMO1")

#### Game variables fps, ground scroll, etc...####
fps = 60
ground_scroll = 0
ground_vel = 5
cool_down = 5
max_rotation = 25
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1000  # milliseconds
last_pipe = pygame.time.get_ticks()
collide = True
is_stop = False


#### ALL THE IMAGE PIPE, GROUND, BACKGROUND, etc....#####
BG = pygame.image.load(os.path.join("assets", "bg.png"))
GROUND = pygame.image.load(os.path.join("assets", "ground.png"))
PIPE = pygame.image.load(os.path.join('assets', "pipe.png"))
MESSAGE = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'message.png')), (300, 300))
INTRO_MUSIC = pygame.mixer.Sound(os.path.join('sound', "INTROMUSIC.mp3"))
WAV = pygame.mixer.Sound(os.path.join('sound', "wing.wav"))
HIT = pygame.mixer.Sound(os.path.join('sound', 'hit.wav'))

#### Create a Bird class: ####


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 4):
            img = pygame.image.load(f'assets/bird{num}.png')
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = 0
        self.counter = 0
        self.tick_count = 0
        self.height = self.rect.y
        self.tilt = 0

    def update(self):
        """
        Rewrite the update of sprite all movement of the bird, gravity,animation,etc...
        """
        # Handle the wing flap of the bird:
        self.counter += 1
        if self.counter < cool_down:
            self.image = self.images[0]
        elif self.counter < cool_down * 2:
            self.image = self.images[1]
        elif self.counter < cool_down * 3:
            self.image = self.images[2]
        elif self.counter < cool_down * 4:
            self.image = self.images[0]
        elif self.counter == cool_down * 4 + 1:
            self.image = self.images[1]
            self.counter = 0
        if flying == False and game_over == True:
            self.image = self.images[1]

        #### -----------------#######

        if flying == True:
            # Gravity
            self.tick_count += 1
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 732:
                self.rect.y += self.vel
            # tilt the bird:
            if self.vel < 0 or self.rect.y < self.height + 50:
                if self.tilt < max_rotation:
                    self.tilt = max_rotation
            else:
                if self.tilt > -90:
                    self.tilt -= max_rotation
            if self.tilt <= -80:
                self.image = self.images[1]
                self.counter = cool_down * 2

            #### jumping movement: using mouse clicked to move up the flappy or Space ####
            if is_stop == False:
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == 0:
                    self.vel = -10.5
                    self.clicked = 1
                    WAV.play()
                if pygame.key.get_pressed()[pygame.K_SPACE] and self.clicked == 0:
                    self.vel = -10.5
                    self.clicked = 1
                    WAV.play()
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = 0

        #### Rotated the bird (stack overflow): ####
        rotated_image = pygame.transform.rotate(self.image, self.tilt)
        new_rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=(self.rect.x, self.rect.y)).center)
        WIN.blit(rotated_image, new_rect)

##### Create a Pipe class: #####


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = PIPE
        self.rect = self.image.get_rect()
        # Position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y-(pipe_gap//2)]
        if position == -1:
            self.rect.topleft = [x, y+(pipe_gap//2)]

    def update(self):
        """
        Rewrite the update function of Sprite
        """
        self.rect.x -= ground_vel
        if self.rect.x < -100:
            self.kill()


##### Sprite Group bird, pipe, etc...: #####
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, HEIGHT//2)
bird_group.add(flappy)

#### FLash effect when bird hit the pipe : ####


def flash_screen():
    flash = pygame.Surface((WIDTH, HEIGHT))
    flash.fill((255, 255, 255))
    WIN.blit(flash, (0, 0))
    pygame.display.update()

### ======STARTING MENU========#####


def welcome_screen():
    """
    welcome screen where the game start.
    """
    ground_scroll_1 = 0
    ground_vel_1 = 5
    clock = pygame.time.Clock()
    run = True

    #### Drawing the Rectangle  for playing button: #####
    play_button = pygame.Rect(WIDTH//2-30, HEIGHT//2-70, 150, 150)

    #### main loop ####
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                run = False
                pygame.quit()
                sys.exit()
            # DEAL with the hover of the mouse:
            # This will make the cursor to arrow again if we move out our cursor from play_button
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            # checking if mouse is collided with the play button
            if pygame.mouse.get_pos()[0] > play_button[0] and\
                    pygame.mouse.get_pos()[0] < play_button[0] + play_button[2]:

                if pygame.mouse.get_pos()[1] > play_button[1] and\
                        pygame.mouse.get_pos()[1] < play_button[1] + play_button[3]:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if play_button.collidepoint(pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN and\
                        event.button == 1:  # checking if mouse has been clicked
                    INTRO_MUSIC.stop()
                    main()

        WIN.blit(BG, (0, 0))
        WIN.blit(MESSAGE, (275, 200))
        WIN.blit(GROUND, (ground_scroll_1, 732))
        ground_scroll_1 -= ground_vel_1
        if abs(ground_scroll_1) > 36:
            ground_scroll_1 = 0

        bird_group.update()
        INTRO_MUSIC.play()

        pygame.display.update()
        clock.tick(fps)

#### =========EXIT MENU========####


def gameOver():
    """
    This game over menu will pop up when the bird collide with pipe or ground.
    """
    # Reset all the variables to zero to reset the game :
    pipe_group.empty()
    score = 0
    flappy.rect.y = HEIGHT//2
    flappy.rect.x = 100
    return score

### =======MAIN GAME=======###


def main():
    """
    main function where the game is running.
    """
    global ground_scroll, ground_vel, game_over, flying, last_pipe,\
        pipe_frequency, collide, is_stop
    run = True
    clock = pygame.time.Clock()

    #### main loop:####
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and game_over == False and flying == False:
                flying = True
            if event.type == pygame.KEYDOWN and game_over == False and flying == False:
                flying = True
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                run = False
                pygame.quit()
                sys.exit()

        #### Draw a Back ground, Ground, bird, etc....####
        WIN.blit(BG, (0, 0))
        pipe_group.draw(WIN)
        WIN.blit(GROUND, (ground_scroll, 732))
        bird_group.update()

        if flappy.rect.bottom > 732 and is_stop == False:
            flash_screen()
            # Set a timer to hide a flash after duration:
            flash_start = pygame.time.get_ticks()
            while pygame.time.get_ticks() - flash_start < 100:
                pygame.display.update()
            game_over = True
            flying = False
            is_stop = True
            HIT.play()
        if flappy.rect.bottom > 732 and is_stop == True:
            flying = False

        #### Look for the collision:####
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) and collide == True:
            HIT.play()
            flash_screen()
            #### Set a timer to hide a flash after duration:####
            flash_start = pygame.time.get_ticks()
            while pygame.time.get_ticks() - flash_start < 100:
                pygame.display.update()
            collide = False
            game_over = True
            is_stop = True

        if not pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
            collide = True

        if game_over == False and flying == True:
            #### generate new pipes: ####
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-150, 150)
                btm_pipe = Pipe(WIDTH, HEIGHT//2 + pipe_height, -1)
                top_pipe = Pipe(WIDTH, HEIGHT // 2 + pipe_height, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now

            #### Scroll the ground:####
            ground_scroll -= ground_vel
            if abs(ground_scroll) > 36:
                ground_scroll = 0
            pipe_group.update()
        pygame.display.update()


while True:
    welcome_screen()
    main()
