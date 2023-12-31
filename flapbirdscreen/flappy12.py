import pygame
from glob import glob
import random
from flapbirdscreen.functions.score import *
from pygame.locals import *
""" flappy 7
added
flags = DOUBLEBUF

Next:
- flappy launches eggs
- water or air or flames from pipes... or spiders?
- enemy birds
- enemy fire gun people on the ground
- enely aline disks

SCREEN

mainsurface     main surface
screen          secundary surface

"""

pygame.init()
pygame.font.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
mainsurface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE, pygame.DOUBLEBUF)
pygame.display.set_caption("Flappy Py")
w, h = 800, 600
screen = pygame.Surface((800, 600))
screen.convert_alpha()

ratio = HEIGHT / 500
width = int(500 * ratio)
screen_posx = int((WIDTH - 500) // 2)
# mainsurface = pygame.display.set_mode((800, 600), flags)
#
game = Score("score.txt")
# ================== MUSIC ===================== #
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(44100, -16, 2, 512)
pygame.mixer.set_num_channels(32)

# ===============================================
jump = pygame.mixer.Sound("flapbirdscreen/sounds/jump.wav")
jump.set_volume(0.5)
hit = pygame.mixer.Sound("flapbirdscreen/sounds/hit.wav")
blip = pygame.mixer.Sound("flapbirdscreen/sounds/blip.ogg")
hit.set_volume(0.3)
# To play a sound use: play(jump)


def circle():
    global grow, radius

    radius = radius + 1 if grow else radius - 1
    if radius > 100:
        grow = 0
    if radius < 10:
        grow = 1
    pg.draw.circle(screen,
        (0, 255, 0),
        (100, 150),
        radius)

def play(snd):
    "Plays one of the sounds in the sounds folder using play('name')"
    pygame.mixer.Sound.play(snd)
# ============================================== #

# List of songs for the soundtrack
base = pygame.mixer.music
music = ["flapbirdscreen/sounds/" + f
    for f in os.listdir("flapbirdscreen/sounds/")
    if f.startswith("base")]

# ================================================= Soundtrack
def load(file):
    return pygame.image.load(file + ".png").convert_alpha()

def load_random_song():
    song = random.choice(music)
    return song

def soundtrack(play="yes", loop=1):
    "This load a base from sounds directory"
    filename = load_random_song()
    if play == "yes":
        base.load(filename)
    elif play == "stop" and filename != None:
        base.stop()
    if loop == 1 and play == "yes":
        base.play(-1)

# ================================================= Soundtrack

font = pygame.font.SysFont("Arial", 16)


def write2(text_to_show, color="Coral"):
    'write("Start")'
    text = font.render(text_to_show, 1, pygame.Color(color))
    return text

normal_speed = 1
class Sprite(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        super(Sprite, self).__init__()
        global g

        self.x = x
        self.y = y
        self.frames = [load(f[:-4]) for f in glob(file + "*.png")]
        self.framesup = [rotate(f[:-4], 45) for f in glob(file + "*.png")]
        self.image = self.frames[0]
        self.imagefall = rotate("fall", -45)
        self.imagespeed = load("speed")

        self.rect = pygame.Rect(self.x, self.y, 32, 24)
        self.cnt = 0
        self.score = 0
        self.maxscore = int(game.maxscore)
        self.mask = self.make_mask()
        g.add(self)

    def make_mask(self):
        return pygame.mask.from_surface(self.image)

    def update(self):
        global moveup, gameover
        # when moveup animation's faster
        self.cnt += .1
        if self.cnt > len(self.frames) - 1:
            self.cnt = 0
        if not moveup:
            self.image = self.frames[int(self.cnt)]
        else:
            self.image = self.framesup[int(self.cnt)]
        if not gameover:
            self.score += 1
        self.check_collision()


    def check_collision(self):
        global gameover

        for pipe in pipes:
            if pygame.sprite.collide_mask(pipe, self):
                if gameover == 0:
                    play(hit)
                    if self.score > self.maxscore:
                        game.save_score(self.score)
                gameover = 1





class Bg(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        global g

        super(Bg, self).__init__()
        self.x = x
        self.y = y
        self.image = load(file)
        self.rect = pygame.Rect(self.x, self.y, w, h)
        g.add(self)


def flip(file):
    return pygame.transform.flip(load(file), 0, 1).convert_alpha()


# loads all different type of pipes
pipes_images = [load("flapbirdscreen/pipes/" + f[:-4]) for f in os.listdir("flapbirdscreen/pipes")]
image1 = pipes_images[random.randint(0, (len(pipes_images) - 1))]

# load different backgrounds
bgs = [load("flapbirdscreen/bg/" + f[:-4]) for f in os.listdir("flapbirdscreen/bg")]
bg1 = bgs[random.randint(0, (len(bgs) - 1))]

class Pipe(pygame.sprite.Sprite):
    def __init__(self, file, x, y, pos=0):
        global g, pipes, lasty

        super(Pipe, self).__init__()

        self.x = x + random.randint(300, 400)
        self.pos = pos
        self.y = random.randint(300, 400)
        self.speed = normal_speed

        if self.pos == 0:
            self.image = image1
            self.rect = pygame.Rect(self.x, self.y, 52, 320)
        else:
            self.image = image1
            self.rect = pygame.Rect(self.x, self.y, 52, 320)
            self.rect.bottom = self.y - random.randint(150, 300)
        pipes.add(self)
        g.add(self)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):

        self.rect.left -= self.speed
        if self.rect.left < -200:
            self.rect.left = 800 + random.randint(50, 100)
            self.y = random.randint(300, 400)
            if self.pos == 0:
                self.rect.top = self.y
            else:
                # DISTANCE AMONG PIPES
                self.rect.bottom = self.y - random.randint(150 - flappy.score // 100, 300 - flappy.score // 100)



class Terrain(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        global g

        super(Terrain, self).__init__()
        self.x = x
        self.y = y
        self.image = load(file)
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.speed = normal_speed
        g.add(self)

    def update(self):
        self.rect.left -= self.speed
        if self.rect.left < -700:
            self.rect.left = 798





def rotate(file, angle):
    return pygame.transform.rotate(load(file), angle)


def gravity(sprite):
    sprite.rect.top += 1

# =========================== Tutorial 3 - change 1


def start():
    global g, pipes, flappy, terrain1, terrain2, bg_surface



    bg_surface = Bg("bg_3", 0, 0)
    pipes = pygame.sprite.Group()

    Pipe("pipe", 200, 300, 0)
    Pipe("pipe", 300, 300, 0)
    Pipe("pipe", 400, 300, 0)
    Pipe("pipe", 500, 300, 0)
    Pipe("pipe", 600, 300, 0)
    Pipe("pipe", 700, 300, 0)
    Pipe("pipe", 800, 300, 0)
    Pipe("pipe", 900, 300, 0)
    Pipe("pipe", 1000, 300, 0)
    Pipe("pipe", 1100, 300, 0)
    # Upside down
    Pipe("pipe", 200, 0, 1)
    Pipe("pipe", 300, 0, 1)
    Pipe("pipe", 400, 0, 1)
    Pipe("pipe", 500, 0, 1)
    Pipe("pipe", 600, 0, 1)
    Pipe("pipe", 700, 0, 1)
    Pipe("pipe", 800, 0, 1)
    Pipe("pipe", 900, 0, 1)
    Pipe("pipe", 1000, 0, 1)
    Pipe("pipe", 1100, 0, 1)

    terrain = random.choice(["terrain_4", "terrain_5"])
    terrain1 = Terrain(terrain, 800, 570)
    terrain2 = Terrain(terrain, 0, 570)
    flappy = Sprite("blue", 300, 300)
    main()

down_cnt = 0
def main():
    global moveup, gameover, movedown, down_cnt
    global g, pipes, flappy, terrain1, terrain2, image1, image2, bg_surface

    # jump controlo variables:
    # - after you press
    moveup = 0
    movedown = 0

    # =================== tutorial 4 - change 1
    gameover = 0
    # how high can go
    startcounter = 0
    # How hight flappy jumps
    topjump = 30
    # how speed it jumps
    jumpspeed = 2
    screen.fill((0, 0, 0))
    # ============ p.5
    text = write2("Score")
    clock = pygame.time.Clock()
    loop = 1
    speedup = 0
    normal_speed = 2
    while loop:

        if flappy.score % 1000 == 0:
            soundtrack()
            normal_speed += 1
            play(blip)
            image1 = pipes_images[random.randint(0, (len(pipes_images) - 1))]
            for pipe in pipes:
                pipe.image = image1
            bg1 = bgs[random.randint(0, (len(bgs) - 1))]
            bg_surface.image = bg1


        if speedup:
            terrain1.speed = 10
            terrain2.speed = 10
            for pipe in pipes:
                pipe.speed = 10
                moveup = 1
            flappy.image = flappy.imagespeed
        else:
            terrain1.speed = normal_speed
            terrain2.speed = normal_speed
            for pipe in pipes:
                pipe.speed = normal_speed

        if moveup:
            flappy.rect.top -= jumpspeed
            startcounter += 1
            # fly faster
            flappy.cnt += .5
            # print(startcounter)
        if startcounter == topjump:
            startcounter = 0
            moveup = 0

        if gameover:
            # cannot fly
            moveup = 0
            # goes down
            flappy.rect.top += 1
            flappy.cnt = 0
            flappy.image = flappy.imagefall
            if flappy.rect.top > 600:
                flappy.kill()
                menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                play(jump)
                moveup = 1
                startcounter = 1
            if event.type == pygame.JOYBUTTONDOWN:
                play(jump)
                moveup = 1
                startcounter = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    play(jump)
                    moveup = 1
                    startcounter = 1
                if event.key == pygame.K_DOWN:
                    play(jump)
                    flappy.image = flappy.imagefall
                    movedown = 1
                if event.key == pygame.K_LEFT:
                    if flappy.rect.left > 10:
                        flappy.rect.left -= 20
                    moveup = 1
                if event.key == pygame.K_RIGHT:
                    if flappy.rect.right < 300:
                        flappy.rect.right += 10
                    play(jump)
                    speedup = 1
                if event.key == pygame.K_ESCAPE:
                    loop = 0
                if event.key == pygame.K_m or event.key == pygame.K_s:
                    flappy.kill()
                    menu()

            # When you do not do nothing

            if event.type == pygame.KEYUP:
                moveup = 0
                speedup = 0
            if event.type == pygame.MOUSEBUTTONUP:
                moveup = 0
            if event.type == pygame.JOYBUTTONUP:
                moveup = 0


        g.draw(screen)
        g.update()

        screen.blit(flappy.image, (0, 0))
        screen.blit(text, (50, 0))
        screen.blit(write2(str(flappy.score), color="White"), (100, 0))
        screen.blit(write2(str(flappy.maxscore), color="White"), (150, 0))

        if not moveup:
            gravity(flappy)
        if movedown: # this is the effective one
            down_cnt += 1
            flappy.rect.top += 3
            if down_cnt == 3:
                movedown = 0
                down_cnt = 0
        mainsurface.blit(pygame.transform.scale(screen, (WIDTH, HEIGHT)), (0, 0))
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def render_multiline(data):
        """Shows a multiline string with text, y pos and color for each line separated by comma"""
        tc = []
        for line in data.split("\n"):

            if line != "":
                text, height, color = line.split(",")
                if height == " " or height == "":
                    height = 0
                    if color == " " or color == "":
                        color = "red"
                else:
                    height = int(height)
                tc.append([text, height, color])
        # 2. Each list of the list above is send to write to render text
        cnt = 0
        for t, height, c in tc:
            cnt += 40
            # calls write passing the text, the vertical position and the color
            for i in t.split("\n"):
                if height == 0:
                    height = cnt
                write(i, 200, height, color=c)
                height += 30


TEXT1 = """*** FLAPPY BIRD ***, , gold
A Game by Giovanni Gatto, , red
,,
Sponsored by,,
pythonprogramming.altevista.org, , coral

,,
Commands, , green

s key: go back to the menu,,gold

Arrow up: fly up, , coral
Arrow right: fly fast, , coral
Arrow left: fly back, , coral
Arrow down: go down, , coral
,,
************ Version 1.9.0 - April 2021 *************, , gray"""


def write(text, x, y, color="Coral",):
    "Returns a surface with a text in the center of the screen, at y coord."
    # renders a font object with a text (this return a surface with a text)
    surface_text = font.render(text, 1, pygame.Color(color))
    # get the center of the text with get_rect (from surface)
    text_rect = surface_text.get_rect(center=(500 // 2, y))
    # show on the screen the surface with text at the text_rect corrdinates in the center
    screen.blit(surface_text, text_rect)
    return surface_text

def exit():
    pygame.quit()
    import sys
    sys.exit()


def splash_page():
    """ The Starting page """

    bb = pygame.image.load("flapbirdscreen/bg_3.png")
    fl = pygame.image.load("flapbirdscreen/bluebird-downflap.png")
    fl = pygame.transform.scale(fl, (100, 64))
    # flappy = Sprite("blue", 30, 500)
    screen.blit(bb, (0, 0))
    render_multiline(TEXT1)
    screen.blit(fl, (500, 300))
    soundtrack()


def menu():
    """ This is the menu that waits you to click the s key to start """

    splash_page()
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_s:
                    start()
            if event.type == pygame.JOYBUTTONDOWN:
                start()
        mainsurface.blit(pygame.transform.scale(screen, (WIDTH, HEIGHT)), (0, 0))
        pygame.display.update()
    pygame.quit()

# ======================= JOYSTICK ===============
def joystick_init():
    """ To initialize joystick """

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        print(joystick.get_name())
    return joysticks


joysticks = joystick_init()
# =========================================joysticks (end)


g = pygame.sprite.Group()
# then goese to start()

'''  FLOW CHART
menu()
    start()
TORUN

menu()


'''