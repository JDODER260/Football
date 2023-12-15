import pygame,random
from pygame.locals import *

xmax = 1000    #width of window
ymax = 600     #height of window

class Particle():
    def __init__(self, startx, starty, col, pause):
        self.x = startx
        self.y = starty
        self.col = col
        self.sx = startx
        self.sy = starty
        self.pause = pause
        self.radius = random.randrange(2,6)

    def move(self):
        if self.pause==0:
            if self.y < 0:
                self.x=self.sx
                self.y=self.sy

            else:
                self.y-=1

            self.x+=random.randint(-2, 2)

        else:
            self.pause-=1
A = 100
black = (255,255,255)
gray = (255,255,0)
B = 380



def main():
    pygame.init()
    screen = pygame.display.set_mode((0,0))
    white = (255, 255, 255)
    black = (255,0,0)
    grey = (255,255,0)

    clock=pygame.time.Clock()

    particles = []
    for part in range(1, A):
        if part % 2 > 0: col = black
        else: col = gray
        particles.append(Particle(515, B, col, round(B*part/A)))

    exitflag = False
    while not exitflag:
        for event in pygame.event.get():
            if event.type == QUIT:
                exitflag = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exitflag = True

        #screen.fill(black)
        for p in particles:
            p.move()
            pygame.draw.circle(screen, p.col, (p.x, p.y), p.radius)
            if random.random() > 0.5:
                if p.radius > 0:
                    p.radius -= .1
            else:
                if p.radius < 6:
                    p.radius += .1

        pygame.display.flip()
        clock.tick(50)
    pygame.quit()

if __name__ == "__main__":
    main()