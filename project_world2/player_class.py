import pygame
from music_module import *
from pathfinding import *
import random
from levels import *
import math

pygame.init()

font = pygame.font.Font('fonts/Трафарет ГОСТ 14192- 96.ttf', 50)
floor_list  = pygame.sprite.Group()



wall = pygame.transform.scale(pygame.image.load("images/wall.png"), (50,50))
decor = pygame.image.load("images/dec.png")
floor = pygame.transform.scale(pygame.image.load("images/floor.png"), (50,50))
yashcik =  pygame.transform.scale(pygame.image.load("images/yashcik.png"), (50,50))
grass =  pygame.transform.scale(pygame.image.load("images/grass.png"), (50,50))
explosion = [] 
desk = pygame.transform.scale(pygame.image.load("images/desk.png"), (50,50))
walls_group = pygame.sprite.Group()
chair = pygame.transform.scale(pygame.image.load("images/chair.png"), (50,50))
printer = pygame.transform.scale(pygame.image.load("images/printer.png"), (50,50))
killed = pygame.transform.scale(pygame.image.load("images/killed.png"), (50, 50))
player1 = pygame.image.load("images/player1.png")
player2 = pygame.image.load("images/player2.png")
not_col = ["floor", "grass"]
washer = pygame.transform.scale(pygame.image.load("images/washer.png"), (50, 50))
special = pygame.transform.scale(pygame.image.load("images/special.png"), (50, 50))
damage_img = pygame.transform.scale(pygame.image.load('images/damage_img.png'), (1500, 1000))
main_server = pygame.transform.scale(pygame.image.load("images/main_server.png"), (50, 50))
lighting = pygame.transform.scale(pygame.image.load("images/lighting.png"), (50, 50))




class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.speed = 25
        self.attack_type = 'basic'
        self.damage = 15
        self.bullets = 25
        self.max_bullets = 25
        self.bullet_speed = 30
        self.dash_length = 200
        self.power = 100
        self.bullet_length = 400
        self.bullet_move = 30
        self.image = player1
        self.image2 = player2
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300
        self.bullet_list = []
        self.bullet_speed_bonus = 0
        self.bullets_amount = 50
        self.anim_rel = 10
        self.img_cur = self.image
        self.anim = False

    def update(self, dis, objs, walls, nexts):

        global game
        scene = 1

        if self.attack_type == 'rpg':
            self.max_bullets = 3
            if self.bullets > 3:
                self.bullets = 3

            self.bullet_speed = 13 + self.bullet_speed_bonus
            self.damage = 255
            self.bullet_length = 300
            self.bullet_move = 200


        if self.attack_type == 'basic':
            self.max_bullets = 25
            if self.bullets > 25:
                self.bullets = 25

            self.bullet_speed = 30 + self.bullet_speed_bonus
            self.damage = 15
            self.bullet_length = 400
            self.bullet_move = 30

        if self.attack_type == 'sniper':
            self.max_bullets = 20
            if self.bullets > 20:

                self.bullets = 20

            self.bullet_speed = 60 + self.bullet_speed_bonus
            self.damage = 150
            self.bullet_length = 800
            self.bullet_move = 100

        if self.attack_type == 'lazer':
            self.max_bullets = -1
            if self.bullets > -1:
                self.bullets = -1

            self.bullet_speed = 50 + self.bullet_speed_bonus
            self.damage = 50
            self.bullet_length = 200
            self.bullet_move = 20



        #player move and attack

        key = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        

        if key[pygame.K_w]:
            self.rect.y -= self.speed
            self.image = pygame.transform.rotate(player1, 90)
            self.image2 = pygame.transform.rotate(player2, 90)
            self.anim_rel -= 1
            for o in walls:
                if self.rect.colliderect(o) and o.typew not in not_col:
                    self.rect.y += self.speed

            if key[pygame.K_LCTRL] and self.power > 0:
                self.rect.y -= self.dash_length
                self.power -= 50

        if key[pygame.K_s]:
            self.rect.y += self.speed
            self.image = pygame.transform.rotate(player1, -90)
            self.image2 = pygame.transform.rotate(player2, -90)
            self.anim_rel -= 1
            for o in walls:
                if self.rect.colliderect(o) and o.typew not in not_col:
                    self.rect.y -= self.speed
            if key[pygame.K_LCTRL] and self.power > 0:
                self.rect.y += self.dash_length
                self.power -= 50

        if key[pygame.K_d]:
            self.rect.x += self.speed
            self.image = player1
            self.image2 = player2
            self.anim_rel -= 1
            for o in walls:
                if self.rect.colliderect(o) and o.typew not in not_col:
                    self.rect.x -= self.speed
            if key[pygame.K_LCTRL] and self.power > 0:
                self.rect.x += self.dash_length
                self.power -= 50

        if key[pygame.K_a]:
            self.rect.x -= self.speed
            self.image = pygame.transform.rotate(player1, 180)
            self.image2 = pygame.transform.rotate(player2, 180)
            self.anim_rel -= 1
            for o in walls:
                if self.rect.colliderect(o) and o.typew not in not_col:
                    self.rect.x += self.speed
            if key[pygame.K_LCTRL] and self.power > 0:
                self.rect.x -= self.dash_length
                self.power -= 50

        if key[pygame.K_LSHIFT]:
            self.speed = 50
        else:
            self.speed = 20

        if player.attack_type == 'lazer':
            if key[pygame.K_UP]:
                player.bullet_list.append(Bullet(player.rect.x, player.rect.y, 'up', self.rect.y))

            if key[pygame.K_DOWN]:
                player.bullet_list.append(Bullet(player.rect.x, player.rect.y, 'down', self.rect.y))

            if key[pygame.K_RIGHT]:
                player.bullet_list.append(Bullet(player.rect.x, player.rect.y, 'right', self.rect.x))

            if key[pygame.K_LEFT]:
                player.bullet_list.append(Bullet(player.rect.x, player.rect.y, 'left', self.rect.x))

            if mouse[0]:
                print(pygame.mouse.get_pos())

        


        for b in self.bullet_list:
            b.update2(dis, self)

        

        if self.anim_rel == 0:
            if self.anim:
                self.anim = False
            else:
                self.anim = True

            self.anim_rel = 10

        if self.anim:
            self.img_cur = self.image2
        else:
            self.img_cur = self.image


        for o in objs:
            if self.rect.colliderect(o.rect):
                if o.type == "pick":
                    text = font.render(f'{o.name}  press E to pickup', False, (0,0,0))
                    dis.blit(text, (50, 170))
                    if key[pygame.K_e]:
                        o.pickup(self)
                elif o.type == "next":
                    text = font.render(f'press E to go to next lvl', False, (0,0,0))
                    dis.blit(text, (50, 170))
                    if key[pygame.K_e]:
                        scene = o.next_scene(nexts)

                

        if self.health < 1:
            scene = -13


        dis.blit(self.img_cur, cam.apply(self))

        pygame.draw.rect(dis, (0, 255, 0), (50, 50, self.health * 4, 50))
        pygame.draw.rect(dis, (0, 0, 255), (50, 125, self.power * 3, 25))
        dis.blit(font.render(self.attack_type, False, (0, 225, 0)), (40, 930))
        dis.blit(font.render(f"патронов: {self.bullets} из {self.max_bullets}  всего: {self.bullets_amount}", False, (0, 225, 0)), (140, 930))

        if self.power < 100:
            self.power += 0.25



        return scene


    def reload(self):
        if self.bullets_amount > self.max_bullets:
            minus = self.max_bullets - self.bullets
            self.bullets = self.max_bullets
            self.bullets_amount -= minus

        else:
            self.bullets += self.bullets_amount
            self.bullets_amount = 0

    



pathfinder = Pathfinder(walls_group)
        


player = Player()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x, y, sight, first_c):

        self.sight = sight
        self.first = first_c

        super().__init__()


        if self.sight == 'right' or self.sight == 'left':
            self.image = pygame.Surface((10, 5))
            self.image.fill((0, 225, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.image = pygame.Surface((5, 10))
            self.image.fill((0, 225, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def update2(self, dis, player):
        dis.blit(self.image, cam.apply(self))

        if self.sight == 'up':

            if self.rect.y > self.first - player.bullet_length:

                self.rect.y -= player.bullet_speed
            else:
                self.kill()
                del player.bullet_list[0]

        if self.sight == 'down':

            if self.rect.y < self.first + player.bullet_length:

                self.rect.y += player.bullet_speed
            else:
                self.kill()
                del player.bullet_list[0]

        if self.sight == 'right':

            if self.rect.x < self.first + player.bullet_length:

                self.rect.x += player.bullet_speed
            else:
                self.kill()
                del player.bullet_list[0]

        if self.sight == 'left':

            if self.rect.x > self.first - player.bullet_length:

                self.rect.x -= player.bullet_speed
            else:
                self.kill()
                del player.bullet_list[0]


class Impact(pygame.sprite.Sprite):
    def __init__(self, damage, x, y):
        super().__init__()
        self.num_of_damage = damage
        self.timer_living = 20
        self.rect = pygame.Rect(x, y, 10, 10)
        self.rect.x = x
        self.rect.y = y
        self.font = pygame.font.Font('fonts/Трафарет ГОСТ 14192- 96.ttf', 20)
        

    def update(self, dis):
        self.text = self.font.render(str(self.num_of_damage), False, (0,0,0),)
        
        self.rect.y -= 1
        dis.blit(self.text, cam.apply(self))
        self.timer_living -= 1
        if self.timer_living == 0:
            self.kill()

impacts = pygame.sprite.Group()        

enemy_group = pygame.sprite.Group()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, size, speed, x, y, pathfinder):
        super().__init__()

        self.health = health
        self.size = size
        self.image = pygame.surface.Surface(self.size)
        self.image.fill((self.health, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.find_player = False
        self.damage = 2
        self.died = False
        self.path = []
        self.pathfinder = pathfinder
        self.recalculate_counter = 0
        self.avoid_radius = 50
        self.damage_plus = 0
        self.speed_plus = 0
        
        

    
    


    def update(self, dis, player, walls):
        
        if not self.died:
            for b in player.bullet_list:
                if self.rect.colliderect(b.rect):
                    self.health -= player.damage
                    player.bullet_list.remove(b)
                    impacts.add(Impact(player.damage, self.rect.x, self.rect.y))



                    if b.sight == 'right':
                        self.rect.x += player.bullet_move
                        
                    if b.sight == 'left':
                        self.rect.x -= player.bullet_move
                        

                    if b.sight == 'down':
                        self.rect.y += player.bullet_move
                        
                    if b.sight == 'up':
                        self.rect.y -= player.bullet_move
                    
                    self.find_player = True

        if self.health < 1 and not self.died:
            self.image = killed
            self.died = True
            self.damage = 0
            if player.health < 81:
                player.health += 20
            killf()
            player.bullets_amount += 20


        if abs(self.rect.x - player.rect.x) < 300 and abs(self.rect.y - player.rect.y) < 300:
                self.find_player = True

        if self.rect.colliderect(player.rect) and not self.died:
            player.health -= self.damage
            dis.blit(damage_img, (0,0))


        if self.find_player and not self.died:
            if player.rect.x > self.rect.x:
                self.rect.x += self.speed
            if player.rect.x < self.rect.x:
                self.rect.x -= self.speed



        dis.blit(self.image, cam.apply(self))

        
        

        
        

        







enemy_group.add(Enemy(255, (50, 50), 7, 800, 500, pathfinder))
enemy_group.add(Enemy(255, (50, 50), 7, 1900, 925, pathfinder))

class Object_pickup_types(pygame.sprite.Sprite):
    def __init__(self, name, x, y, type):
        super().__init__()

        self.name = name
        self.image = pygame.image.load("images\item-pickup.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.type = type

    def update(self, dis):
        dis.blit(self.image, cam.apply(self))

    def pickup(self, player):

        player.attack_type = self.name
        
        player.reload()

        pickup()
        
        self.kill()

    def next_scene(self, scene):
        pickup()

        return scene

        


#, speed, damage, bullets: bool, bullets_length, bullet_speed


objs_group = pygame.sprite.Group()
objs_group.add(Object_pickup_types("down", 2450, 625, "next"))







class Map_class1():
    def __init__(self):


        self.map_r =   level1


        self.level_2 = level2

        self.level_3 = level3
        self.level_4 = level4

    def draw_map(self, group):
        y = 0
        x = 0
        for line in self.map_r:
            for s in line:
                if s == "11":
                    floor_list.add(Floor(x, y))
                if s == "1":
                    group.add(Wall("wall", x, y))
                
                if s == "2":
                    group.add(Wall("decor", x, y))

                if s == '0':
                    floor_list.add(Floor(x, y))

                if s == "3":
                    group.add(Wall("yashcik", x, y))
                
                if s == "4":
                    floor_list.add(Wall("grass", x, y))
                
                if s == "6":
                    group.add(Wall("chair", x, y))
                if s == "7":
                    group.add(Wall("printer", x, y))
                if s == "9":
                    group.add(Wall("washer", x, y))
                if s == "8":
                    group.add(Wall("special", x, y))
                if s == "10":
                    group.add(Wall("main_server", x, y))
                


                
                x += 50

            x = 0
            y += 50

    def change2(self):
        self.map_r = self.level_2
    def change3(self):
        self.map_r = self.level_3
    def change4(self):
        self.map_r = self.level_4


class Wall(pygame.sprite.Sprite):
    def __init__(self, typew, x, y):
        super().__init__()
        self.typew = typew
        if typew == "wall":
            self.img = wall
        elif typew == "decor":
            self.img = desk
        elif typew == "yashcik":
            self.img = yashcik
        elif typew == "grass":
            self.img = grass
        elif typew == "chair":
            self.img = chair
        elif typew == "printer":
            self.img = printer
        elif typew == "washer":
            self.img = washer
        elif typew == "special":
            self.img = special
        elif typew == "main_server":
            self.img = main_server
        elif typew == "lighting":
            self.img = lighting
        


        
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self, player, dis):
        dis.blit(self.img, cam.apply(self))

        for b in player.bullet_list:
            if self.rect.colliderect(b.rect) and self.typew not in not_col:
                player.bullet_list.remove(b)


map_obj = Map_class1()

class Floor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img = floor
        self.rect = self.img.get_rect()
        self.rect.x= x
        self.rect.y = y

    def update(self,player, dis):
        dis.blit(self.img, cam.apply(self))
    


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)
	
    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)
    
    
def camera_configure(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l+1500 / 2, -t+1000 / 2

        l = min(0, l)                           # Не движемся дальше левой границы
        l = max(-(camera.width-1500), l)   # Не движемся дальше правой границы
        t = max(-(camera.height-1000), t) # Не движемся дальше нижней границы
        t = min(0, t)                           # Не движемся дальше верхней границы

        return pygame.Rect(l, t, w, h)


cam = Camera(camera_configure, len(map_obj.map_r[0]) * 50, len(map_obj.map_r) * 50)