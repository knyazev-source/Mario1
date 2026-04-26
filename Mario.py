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
        self.location = ['45-310','440-260','440-400','45-400','440-100','620-90','240-110','620-250','240-210']
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
    def loct(self):
        elm = choice(self.location)
        self.location.remove(elm)
        elm = elm.split('-')
        self.rect.x = int(elm[0])
        self.rect.y = int(elm[1])

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
'''Убранно за ненадобностю в классе все
acl = 0
a = 0
q=0
i = False'''



'''mixer.init()
mixer.music.load('saundtrek.mp3')
#mixer.music.play()
jump = mixer.Sound('jump.mp3')
money = mixer.Sound('money.mp3')
over = mixer.Sound('over.mp3')
gamo = mixer.Sound('gamo.mp3')'''

# Создание платформ
platforms = [] # Делаем препятствия в списке
earth = Wall(0,450,700,50)
cell = Wall(0,-1,800,1)
plat1 = Wall(580,130,100,25)
plat2 = Wall(400,300,100,25)
plat3 = Wall(20,100,100,25)
plat4 = Wall(200,150,100,25)
plats = Wall(20,350,70,20)
platforms.extend([earth, cell,plats , plat1, plat2, plat3, plat4]) # Переношу платформы в список

coin = Coin()
coin.loct()
coin.location.append('60-60')

player = Player('Mario.png',30,299,4) # Сменил 3 на 4 вкусовщина
#prev_rect = player.rect.copy() Отключенно за ненадобностью

while run:
    window.blit(background,(0,0))
    for e in event.get():
        keys = key.get_pressed()
        if e.type == QUIT:
            run = False

    # Рисуем
    for plat in platforms:
        plat.reset()

    # Движение и отрисовка игрока
    player.move(platforms)
    player.reset()
    
    coin.reset()


    clock.tick(60)
    display.update()
    #У меня еще огромные планы на этот проект
'''Логика прыжка в классе
        if e.type == KEYDOWN and keys[K_UP]:
            print(0)
            #когда нажимаю кнопку прышка напишет 0
            if i:
                player.rect.y-=10
                acl = -4.8'''



'''Частично перенесенно в класс частично переработка
player.speed = 3
    if sprite.collide_rect(player, earth):
        if prev_rect.bottom <= earth.rect.top:
            player.rect.bottom = earth.rect.top
            i = True
            player.speed = 4
            acl = 0 # ускорение
            a = 0 # счетчик'''
        #i = True   Возможный вариант решения проблемы - при прикосновении с любой стороны, но можно будет отпрыгивать от стен(не совсем минус)
'''
    if sprite.collide_rect(player, plat1) or sprite.collide_rect(player, plat2) or sprite.collide_rect(player, plat3):
        if (acl < 0 or acl > 0) and (player.rect.y < plat1.rect.y or player.rect.y < plat2.rect.y or player.rect.y < plat3.rect.y):
            player.rect.y+=20
        print(player.rect.x)
        print(player.rect.y)
        player.speed = 3
        acl = 0
        a = 0
'''

# Проверка коллайда с синим квадратом
'''Анологично все либо в классе либо ненадо
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
'''




''' Что то вынесенно в группы чего то ненадо что то просто в классе лежит
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
    display.update()'''
