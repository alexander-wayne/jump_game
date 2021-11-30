import pygame
import os
import random

from pygame.constants import K_SPACE, KEYDOWN
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

STAT_FONT = pygame.font.SysFont("arial", 50)
GAME_OVER_FONT = pygame.font.SysFont("arial", 30)

PLAYER_IMGS = [
    pygame.image.load(os.path.join("imgs", "player_falling.png")),
    pygame.image.load(os.path.join("imgs", "player_jumping.png")),
]
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
PLATFORM_IMG = pygame.image.load(os.path.join("imgs", "platform.png"))
CARROT_IMG = pygame.image.load(os.path.join("imgs", "carrot.png"))

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Doodle Hop")

class Player:

    IMGS = PLAYER_IMGS

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tick_count = 0
        self.velocity = 0
        self.img_count = 0
        self.current_img = self.IMGS[0]
        self.x_speed = 5
        self.gravity = 8
        self.jump_force = 4.75


    def jump(self):
        self.velocity = -self.jump_force
        self.tick_count = 0
        self.current_img = PLAYER_IMGS[0]

    def move(self):

        self.tick_count += 1

        # for downward acceleration
        displacement = self.velocity*(self.tick_count) + 0.5*(.35)*(self.tick_count)**2  # calculate displacement

        # terminal velocity
        if displacement >= self.gravity:
            displacement = (displacement / abs(displacement)) * self.gravity

        if displacement < 0:
            displacement -= 2
            self.current_img = PLAYER_IMGS[1]

        self.y = self.y + displacement

        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.x_speed
            if self.x < -1:
                self.x = 0
        if keys[pygame.K_RIGHT]:
            self.x += self.x_speed
            if self.x > WIN_WIDTH - self.current_img.get_width() + 1:
                self.x = WIN_WIDTH - self.current_img.get_width()

    def draw(self, win):
        win.blit(self.current_img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.current_img)

class Platform:

    IMG = PLATFORM_IMG
    
    def __init__(self, x):
        self.x = x
        self.y = WIN_HEIGHT - PLAYER_IMGS[0].get_height()

    def move(self):
        self.x = random.randrange(0, WIN_WIDTH - self.IMG.get_width())

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

    def collide(self, player):
        player_mask = player.get_mask()
        platform_mask = pygame.mask.from_surface(self.IMG)

        col_point = player_mask.overlap(platform_mask, (self.x - player.x, self.y - round(player.y)))

        if col_point:
            return True
        return False
    
    
class Carrot:

    IMG = CARROT_IMG
    
    def __init__(self, x):
        self.x = x
        self.y = WIN_HEIGHT / 2 - PLAYER_IMGS[0].get_height()

    def move(self):
        self.x = random.randrange(0, WIN_WIDTH - self.IMG.get_width())

    def draw(self, win):
        win.blit(self.IMG, (self.x, self.y))

    def collide(self, player):
        player_mask = player.get_mask()
        platform_mask = pygame.mask.from_surface(self.IMG)

        col_point = player_mask.overlap(platform_mask, (self.x - player.x, self.y - round(player.y)))

        if col_point:
            return True
        return False
    
    

def draw_window(win, player, platform, carrots, score):
    win.blit(BG_IMG, (0, 0))
    for carrot in carrots:
        carrot.draw(win)
    player.draw(win)
    platform.draw(win)

    score_label = STAT_FONT.render("Score: " + str(score), 1, (0, 0, 0))
    win.blit(score_label, (15, 10))

    pygame.display.update()

def end_screen(win):
    run = True
    game_over_label = GAME_OVER_FONT.render("Game Over :(\nPress a key to restart", 1, (0, 0, 0))

    print("GAME MOVER")
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)
        
        win.blit(game_over_label, (WIN_WIDTH / 2 - game_over_label.get_width() / 2, WIN_HEIGHT / 2 - game_over_label.get_height() / 2))
        pygame.display.update()

    pygame.quit()
    quit()

def main(win):

    player = Player(
        WIN_WIDTH / 2 - PLAYER_IMGS[0].get_width() / 2, 
        WIN_HEIGHT / 2 - PLAYER_IMGS[0].get_height() / 2
    )
    platform = Platform(WIN_WIDTH / 2 - PLATFORM_IMG.get_width() / 2)
    carrots = []
    score = 0
    clock = pygame.time.Clock()
    run = True
    lost = False

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()    

        if not lost:

            player.move()
            if platform.collide(player):
                player.jump()
                platform.move()
                if len(carrots) == 0:
                    carrots.append(Carrot(random.randrange(0, WIN_WIDTH - CARROT_IMG.get_width())))
            
            for carrot in carrots:
                if carrot.collide(player):
                    carrots.clear()
                    score += 1

            
        if(player.y > WIN_HEIGHT + player.current_img.get_height()):
            lost = False
            break

        draw_window(win, player, platform, carrots, score)

    end_screen(WIN)

main(WIN)