import pygame
import sys
import random
pygame.init()

display = pygame.display.set_mode((1000,800))
pygame.display.set_caption("Nočna straža")
pygame.display.set_icon(pygame.image.load("drevo.png"))
clock = pygame.time.Clock()


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def main(self, display):
        pygame.draw.rect(display, (255,0,0), (self.x, self.y, self.width, self.height)), 

class Tree:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
    def draw(self, display, scroll):
        display.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))

class Stick:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image, (100, 100))
    def draw(self, display, scroll):
        display.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))

class Campfire:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(image, (200, 200))
    def draw(self, display, scroll):
        display.blit(self.image, (self.x - scroll[0], self.y - scroll[1]))

class StaminaBar():
    def __init__(self, x, y, width, height, max_stamina,):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.stamina = max_stamina
        self.max_stamina = max_stamina  
    def draw(self, display):    
        ratio = self.stamina / self.max_stamina
        pygame.draw.rect(display, "black", (self.x, self.y, self.width, self.height))
        pygame.draw.rect(display, "white", (self.x+4, self.y+4, (self.width * ratio)-8, self.height-8))

stamina_bar = StaminaBar(325, 600, 400, 30, 100)

tree_list = []
for i in range(100):
    tree = Tree(random.randint(-2000, 2000), random.randint(-2000, 2000), pygame.image.load("drevo.png"))
    tree_list.append(tree)
    tree_list.sort(key=lambda tree: tree.y)

stick_amount = 0
stick_list = []
def spawn_stick():
    stick = Stick(random.randint(-2000, 2000), random.randint(-2000, 2000), pygame.image.load("palca.png"))
    stick_list.append(stick)
    stick_list.sort(key=lambda stick: stick.y)

stick_inv = 0

def check_proximity(px, py, sx, sy, threshold=100):
    distance = ((px - sx) ** 2 + (py - sy) ** 2) ** 0.5
    return distance < threshold

text_font = pygame.font.SysFont("Comic Sans MS", 30)

def draw_text(text, font, text_color, x, y, value=0):
    img = font.render(text + str(value), True, text_color)
    display.blit(img, (x, y))

 
player = Player(500, 400, 32, 32)
campfire = Campfire(500, 400, pygame.image.load("ogenj.png"))

display_scroll = [0,0]

while True:
    display.fill((25,165,85))
    
    if stick_amount < 31:
        if random.randint(1,2) == 1:
            spawn_stick()
            stick_amount += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LSHIFT] and stamina_bar.stamina > 0:
        speed = 6
        stamina_bar.stamina -= 0.5
    else:
        speed = 3
        if stamina_bar.stamina < stamina_bar.max_stamina:
            if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
                stamina_bar.stamina += 0.05
            else:
                stamina_bar.stamina += 0.2
    
    if keys[pygame.K_a]:
        display_scroll[0] -= speed
    if keys[pygame.K_d]:
        display_scroll[0] += speed
    if keys[pygame.K_w]:
        display_scroll[1] -= speed
    if keys[pygame.K_s]:
        display_scroll[1] += speed

    pygame.draw.rect(display, (255,255,255), (100-display_scroll[0], 100-display_scroll[1], 16, 16))

    for tree in tree_list:
        tree.draw(display, display_scroll)

    for stick in stick_list:
        stick.draw(display, display_scroll)

    remaining_sticks = []

    for stick in stick_list:
        if check_proximity(500, 400, stick.x - display_scroll[0], stick.y - display_scroll[1]):
            stick_amount -= 1
            stick_inv += 1

        else:
            remaining_sticks.append(stick)

    stick_list = remaining_sticks

    draw_text("Palce: ", text_font, (255,255,255), 10, 1, stick_inv)

    stamina_bar.draw(display)
    
    campfire.draw(display, display_scroll)
    
    player.main(display)

    clock.tick(60)
    pygame.display.update()
