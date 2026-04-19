from pygame import *

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
i = False



mixer.init()
mixer.music.load('saundtrek.mp3')
#mixer.music.play()
jump = mixer.Sound('jump.mp3')
money = mixer.Sound('money.mp3')
over = mixer.Sound('over.mp3')
gamo = mixer.Sound('gamo.mp3')

earth = Wall(0,450,700,50)
plat1 = Wall(600,130,100,30)
plat2 = Wall(400,300,100,30)
plat3 = Wall(0,666,100,30)
player = Player('Mario.png',20,390,3)
prev_rect = player.rect.copy()

while run:
    window.blit(background,(0,0))
    for e in event.get():
        keys = key.get_pressed()
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and keys[K_UP]:
            print(0)
            #когда нажимаю кнопку прышка напишет 0
            if i:
                player.rect.y-=10
                acl = -4.8



    player.speed = 3
    if sprite.collide_rect(player, earth):
        if prev_rect.bottom <= earth.rect.top:
            player.rect.bottom = earth.rect.top
            i = True
            player.speed = 4
            acl = 0 # ускорение
            a = 0 # счетчик
        #i = True   Возможный вариант решения проблемы - при прикосновении с любой стороны, но можно будет отпрыгивать от стен(не совсем минус)
    '''if sprite.collide_rect(player, plat1) or sprite.collide_rect(player, plat2) or sprite.collide_rect(player, plat3):
        if (acl < 0 or acl > 0) and (player.rect.y < plat1.rect.y or player.rect.y < plat2.rect.y or player.rect.y < plat3.rect.y):
            player.rect.y+=20
        print(player.rect.x)
        print(player.rect.y)
        player.speed = 3
        acl = 0
        a = 0'''

# Проверка коллайда с синим квадратом
    if player.rect.colliderect(plat2.rect):
        # Определяем, с какой стороны произошло столкновение
        if prev_rect.right <= plat2.rect.left:
            # столкновение справа
            player.rect.right = plat2.rect.left
        elif prev_rect.left >= plat2.rect.right:
            # столкновение слева
            player.rect.left = plat2.rect.right
        elif prev_rect.top >= plat2.rect.bottom:
            # столкновение снизу
            player.rect.top = plat2.rect.bottom
            acl = 0
        elif prev_rect.bottom <= plat2.rect.top:
            # столкновение сверху
            player.rect.bottom = plat2.rect.top
            i = True
            player.speed = 4
            acl = 0 # ускорение
            a = 0 # счетчик




    prev_rect = player.rect.copy()

    earth.reset()
    plat1.reset()
    plat2.reset()
    plat3.reset()
    player.reset()
    player.move()




    a+=1
    if a>=3:
        i = False
        player.rect.y+=acl
        acl += 0.07
        player.q = 0
    


    clock.tick(60)
    display.update()


#При нажатии на прыжок не всегда он происходит
#То есть проблема всего скорее в i
