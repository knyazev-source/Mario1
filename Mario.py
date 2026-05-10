from pygame import *
from random import choice

class Game(sprite.Sprite):
    '''Главный класс с основными параметрами'''
    def __init__(self, imag, x, y, speed):
        self.image = transform.scale(image.load(imag),(50,50))
        super().__init__()
        self.rect = self.image.get_rect()
        self.rect.x = int(x)
        self.rect.y = int(y)
        self.speed = int(speed)
        self.q = 0
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(Game): # Наибольшая переработка перенос логики из игрового цикла
    '''Класс персонажа наследник Game'''
    def __init__(self, imag, x, y, speed): # Нужно было внести +3 параметра поэтому создал конструктор
        super().__init__(imag, x, y, speed)
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False # Следим касаемся ли платформ

    def move(self, platforms): # Добавление в логику доп обьекта
        global i
        keys = key.get_pressed()
        
        # Горизонтальное движение
        self.vel_x = 0
        if keys[K_LEFT] and self.rect.x >= 0: # Пока Убрал  and self.rect.x >= 0
            self.vel_x -= self.speed # Вместо self.rect.x -> self.vel_x
            # self.q =1 В новой логике не нужно
        if keys[K_RIGHT] and  self.rect.x <= 650: # делаем if И пока убираю and self.rect.x <= 650
            self.vel_x += self.speed # Анологично 30 строке
            #self.q = 1 В новой логике не нужно
        '''elif keys[K_UP] and self.rect.y >= 0:
            self.rect.y -= 10'''
        '''Ниже доп код переработанный переносящий отслеживание в класс гравитацию и прыжок'''
        self.rect.x += self.vel_x # Движение
        # Проверка горизонтальных столкновений
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel_x > 0:
                    self.rect.right = plat.rect.left
                elif self.vel_x < 0:
                    self.rect.left = plat.rect.right
        # Прыжок
        if keys[K_UP] and self.on_ground:
            self.vel_y = -14
            jump.play()
        # Гравитация
        self.vel_y += 0.5
        self.rect.y += int(self.vel_y)
        # Обновляем состояние для земли
        self.on_ground = False
        # Проверка вертикальных столкновений
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel_y > 0:  # падаем вниз
                    self.rect.bottom = plat.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # летим вверх
                    self.rect.top = plat.rect.bottom
                    self.vel_y = 0

class Monster(Game):
    def __init__(self, imag, x, y, speed, lx, rx):
        super().__init__(imag, x, y, speed)
        self.image = transform.scale(image.load(imag),(35,35))
        self.lx = int(lx)
        self.rx = int(rx)
        self.y = 1
    def move(self):
        if self.rect.x <= self.lx:
            self.y=1
        elif self.rect.x >= self.rx:
            self.y=2
        if self.y==1:
            self.rect.x += self.speed
        if self.y==2:
            self.rect.x -= self.speed

class Coin(sprite.Sprite):
    '''Класс монеток'''
    def __init__(self):
        super().__init__()
        self.color = (186,255,0)
        self.width = 20
        self.heigth = 30
        self.image = Surface((self.width, self.heigth))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.location = ['60-60','440-260','440-400','45-400','440-100','620-90','240-110','620-250','240-210']
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
        if self.rect.colliderect(player.rect):
            self.loct()
    def loct(self):
        if len(self.location) != 0:
            global h
            elm = choice(self.location)
            h = elm
            self.location.remove(elm)
            elm = elm.split('-')
            self.rect.x = int(elm[0])
            self.rect.y = int(elm[1])
        else:
            global dp
            self.rect.x = -100
            self.rect.y = -100
            dp = ['60-60','440-260','440-400','45-400','440-100','620-90','240-110','620-250','240-210','45-310']
            dp.remove(h)
            door.loct()




class Exit(sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.color = (247,247,137)
        self.width = 55
        self.heigth = 70
        self.image = transform.scale(image.load('door1.png'),(55,70))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.i = 1
    def win(self):
        if self.rect.colliderect(player.rect):
            global run
            run = False
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
    def loct(self):
        global dp
        elm = choice(dp)
        dp.remove(elm)
        elm = elm.split('-')
        self.rect.x = int(elm[0])-35/2
        self.rect.y = int(elm[1])-25


class Wall(sprite.Sprite):
    '''Класс стен'''
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


# Настройки окна
display.set_caption("Mario")
window = display.set_mode((700, 500))
background = transform.scale(image.load('Sky.jpg'), (700, 500))
clock = time.Clock()

run = True
count = 0
counter = 0
dcounter = 1
mcounter = 1
font.init()
font = font.Font(None, 36)

mixer.init()
mixer.music.load('saundtrek.mp3')
mixer.music.play()
jump = mixer.Sound('jump.mp3')
money = mixer.Sound('money.mp3')
over = mixer.Sound('over.mp3')
gamo = mixer.Sound('gamo.mp3')

# Создание платформ
platforms = [] # Делаем препятствия в списке
earth = Wall(0,450,700,50)
cell = Wall(0,-1,800,1)
plat1 = Wall(580,130,100,30)
plat2 = Wall(400,300,100,30)
plat3 = Wall(20,100,100,30)
plat4 = Wall(200,150,100,30)
plats = Wall(20,350,70,30)
platforms.extend([earth, cell,plats , plat1, plat2, plat3, plat4]) # Переношу платформы в список

coin = Coin()
coin.loct()
coin.location.append('45-310')

player = Player('Mario.png',30,299,4)
door = Exit(-100,-100)
mn1 = Monster('m1_1.png', 315, 415, 2, 35, 630)
mn2 = Monster('Monster.png', 455, 80, 2, 135, 640)

from time import time
start_time = time()

while run:
    window.blit(background,(0,0))
    for e in event.get():
        keys = key.get_pressed()
        if e.type == QUIT:
            run = False
        if keys[K_q]:
            coin.loct()

    now_time = time()
    timer = 60-int(-1*(start_time - now_time))
    if timer == 0:
        break

    # Рисуем
    for plat in platforms:
        plat.reset()

    # Движение и отрисовка игрока
    door.reset()
    door.win()

    player.move(platforms)
    player.reset()
    
    mn1.move()
    mn1.reset()
    mn2.move()
    mn2.reset()

    coin.reset()

    if player.rect.colliderect(mn1.rect) or player.rect.colliderect(mn2.rect):
        mixer.music.stop()
        over.play()
        run = False

    timer1 = font.render(str(timer),True,(255,0,0))
    window.blit(timer1,(10,10))

    counter += 1
    if counter >= 60:
        dcounter += 1
        if dcounter == 1:
            door.image = transform.scale(image.load('door1.png'),(55,70))
        elif dcounter == 2:
            door.image = transform.scale(image.load('door2.png'),(55,70))
            dcounter = 0
        mcounter += 1
        if mcounter == 1:
            mn1.image = transform.scale(image.load('m1_1.png'),(35,35))
        elif mcounter == 2:
            mn1.image = transform.scale(image.load('m1_2.png'),(35,35))
            mcounter = 0
        
        
        counter = 0
        

    clock.tick(60)
    display.update()
'''
run = True
while run:
    window.blit(background,(0,0))
    for e in event.get():
        keys = key.get_pressed()
        if e.type == QUIT:
            run = False
    clock.tick(180)
    display.update()'''
