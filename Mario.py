from pygame import *
q = 1
class Game(sprite.Sprite):
    def __init__(self, imag, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(imag),(50,50))
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.speed = int(speed)
        self.q = 0
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(Game):

    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
            self.q =1 
        elif keys[K_RIGHT] and self.rect.x <= 650:
            self.rect.x += self.speed
            self.q = 1
        '''elif keys[K_UP] and self.rect.y >= 0:
            self.rect.y -= 10'''


class Wall(sprite.Sprite):
    def __init__(self,x,y,weidth,heidth,color = (11,244,120)):
        super().__init__()
        self.color = color
        self.width = int(weidth)
        self.heigth = int(heidth)
        self.image = Surface((self.width, self.heigth))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

display.set_caption("Mario_Na_Minimalkah")
window = display.set_mode((700, 500))
background = transform.scale(image.load('Sky.jpg'), (700, 500))
clock = time.Clock()
run = True
acl = 0
a = 0
q=0

earth = Wall(0,450,700,50)
plat1 = Wall(600,130,100,30)
plat2 = Wall(400,300,100,30)
plat3 = Wall(0,666,100,30)
player = Player('Mario.png',20,401,3)

while run:
    window.blit(background,(0,0))
    for e in event.get():
        keys = key.get_pressed()
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and keys[K_UP]:
            if sprite.collide_rect(player, earth) or sprite.collide_rect(player, plat1) or sprite.collide_rect(player, plat2) or sprite.collide_rect(player, plat3):
                player.rect.y-=10
                acl = -4.8
            

    earth.reset()
    plat1.reset()
    plat2.reset()
    plat3.reset()
    player.reset()
    player.move()

    player.speed = 3
    if sprite.collide_rect(player, earth):
        player.speed = 3
        acl = 0
        a = 0
    if sprite.collide_rect(player, plat1) or sprite.collide_rect(player, plat2) or sprite.collide_rect(player, plat3):
        if acl < 0 or acl > 0:
            player.rect.y+=80
        player.speed = 3
        acl = 0
        a = 0


    a+=1
    if a>=3:
        player.rect.y+=acl
        acl += 0.07
        player.q = 0
    

    

    clock.tick(60)
    display.update()