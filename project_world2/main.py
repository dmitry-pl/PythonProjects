import pygame
import sqlite3
from music_module import *
from button_saver import *
from player_class import *
from pathfinding import *
from cut_scene import *
from boss import Boss

# Инициализация Pygame и создание окна
pygame.init()
dis = pygame.display.set_mode((1500, 1000))
pygame.display.set_caption('PROJECT_WORLD.EXE')
pygame.display.set_icon(pygame.image.load('images/skull.png'))

# Подключение к базе данных
con = sqlite3.connect('save.db')
cur = con.cursor()

# Текст управления для экрана настроек
contr_text = [
    "w a s d - перемещение", 
    "стрелки - стрельба", 
    "r - перезарядка", 
    "space(зажать) - замедление времени", 
    "e - взаимодейтвовать", 
    "esc - пауза"
]

# Загрузка изображений
back_menu = pygame.transform.scale(pygame.image.load('images/back_menu.png'), (1500, 1000))
death_menu = pygame.transform.scale(pygame.image.load('images/death_menu.png'), (1500, 1000))
time_stop = pygame.transform.scale(pygame.image.load('images/time_stop.png'), (1500, 1000))
time_stop.set_alpha(190)

# Инициализация игровых объектов
clock = pygame.time.Clock()
game = True
scene = -1  # Текущая сцена/экран
time = False  # Флаг замедления времени
saved = False
next_sc = -4  # Следующая сцена
boss_o = Boss()  # Босс
boss_fight = False  # Флаг боя с боссом

# Запуск музыки меню
music_menu()

# Главный игровой цикл
while game:
    dis.fill((200,200,200))
    
    # Обработка событий
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False

        # Обработка событий игрового процесса
        if scene == 1:
            # Стрельба в разных направлениях
            if player.attack_type != 'lazer' and player.bullets > 0:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                    player.bullet_list.append(Bullet(player.rect.x + 25, player.rect.y, 'up', player.rect.y))
                    player.bullets -= 1
                    player.image = pygame.transform.rotate(player1, 90)
                    player.image2 = pygame.transform.rotate(player2, 90)
                    shoot()

                if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                    player.bullet_list.append(Bullet(player.rect.x + 25, player.rect.y + 50, 'down', player.rect.y))
                    player.bullets -= 1
                    player.image = pygame.transform.rotate(player1, -90)
                    player.image2 = pygame.transform.rotate(player2, -90)
                    shoot()

                if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                    player.bullet_list.append(Bullet(player.rect.x + 50, player.rect.y + 25, 'right', player.rect.x))
                    player.bullets -= 1
                    player.image = player1
                    player.image2 = player2
                    shoot()

                if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                    player.bullet_list.append(Bullet(player.rect.x - 25, player.rect.y + 25, 'left', player.rect.x))
                    player.bullets -= 1
                    player.image = pygame.transform.rotate(player1, 180)
                    player.image2 = pygame.transform.rotate(player2, 180)
                    shoot()
            
            # Перезарядка
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r and player.bullets < player.max_bullets:
                player.reload()

            # Замедление времени
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                if player.power > 0.9:
                    for en in enemy_group:
                        en.speed /= 3
                    time = True

            if e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
                if time:
                    for en in enemy_group:
                        en.speed *= 3
                    time = False

        # Обработка катсцен
        if scene == "c1" and e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            scene1.num += 1
        if scene == "c2" and e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            scene2.num += 1
        if scene == "c3" and e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            scene3.num += 1

        # Обработка меню
        if e.type == pygame.MOUSEBUTTONDOWN:
            # Главное меню
            if scene == -1:
                if b_new_game.isOver(pygame.mouse.get_pos()):
                    player.kill()
                    player = Player()
                    scene = -2
                    pygame.mixer.music.stop()
                elif b_continue2.isOver(pygame.mouse.get_pos()):
                    cur.execute("SELECT scene, health, patrons, current_bul, type FROM save")
                    res = cur.fetchall()
                    player.health = res[0][1]
                    player.bullets_amount = res[0][2]
                    player.bullets = res[0][3]
                    player.attack_type = res[0][4]
                    scene = res[0][0]
                    pygame.mixer.music.stop()
            
            # Меню паузы
            elif scene == -3:
                if b_continue.isOver(pygame.mouse.get_pos()):
                    scene = 1
                elif b_about.isOver(pygame.mouse.get_pos()):
                    scene = "about"
                elif b_settings.isOver(pygame.mouse.get_pos()):
                    scene = "controls"
                elif b_menu.isOver(pygame.mouse.get_pos()):
                    scene = -1
                    music_menu()
            
            # Кнопки назад
            elif (scene == "about" or scene == "controls") and b_back.isOver(pygame.mouse.get_pos()):
                scene = -3
            
            # Меню смерти
            elif scene == -13 and b_menu2.isOver(pygame.mouse.get_pos()):
                scene = -1
                music_menu()

        # Пауза по ESC
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE and scene == 1:
            scene = -3

    # Отрисовка сцен
    if scene == -1:  # Главное меню
        dis.blit(back_menu, (0,0))
        b_new_game.draw(dis, pygame.mouse.get_pos())
        b_continue2.draw(dis, pygame.mouse.get_pos())
    
    elif scene == -2:  # Новая игра
        cur.execute("DELETE FROM save")
        cur.execute(f"insert into save(scene, health, patrons, current_bul, type) values(-2, {player.health}, {player.bullets_amount}, {player.bullets}, '{player.attack_type}')")
        con.commit()
        scene = "c1"
        map_obj.draw_map(walls_group)
        pygame.mixer.music.stop()
    
    elif scene == -13:  # Меню смерти
        dis.blit(death_menu, (0,0))
        b_menu2.draw(dis, pygame.mouse.get_pos())
    
    elif scene == -3:  # Меню паузы
        b_continue.draw(dis, pygame.mouse.get_pos())
        b_menu.draw(dis, pygame.mouse.get_pos())
        b_about.draw(dis, pygame.mouse.get_pos())
        b_settings.draw(dis, pygame.mouse.get_pos())
    
    elif scene == "about":  # О игре
        b_back.draw(dis, pygame.mouse.get_pos())
    
    elif scene == "controls":  # Управление
        b_back.draw(dis, pygame.mouse.get_pos())
        y = 140
        for t in contr_text:
            dis.blit(font.render(t, False, (0,0,0)), (40, y))
            y += 100
    
    elif scene == 1:  # Игровой процесс
        cam.update(player)
        floor_list.update(player, dis)
        
        if time:  # Эффект замедления времени
            dis.blit(time_stop, (0,0))
            player.power -= 1
            if player.power < 1:
                time = False
                for e in enemy_group:
                    e.speed *= 3
        
        walls_group.update(player, dis)
        enemy_group.update(dis, player, walls_group)
        impacts.update(dis)
        scene = player.update(dis, objs_group, walls_group, next_sc)
        objs_group.update(dis)
        
        if boss_fight:
            boss_o.update(dis, player)
    
    elif scene == "c1":  # Катсцена 1
        scene = scene1.update(dis)
    elif scene == "c2":  # Катсцена 2
        scene = scene2.update(dis)
    elif scene == "c3":  # Катсцена 3
        scene = scene3.update(dis)
    
    # Переходы между уровнями
    elif scene == -4:  # Переход на уровень 2
        cur.execute("DELETE FROM save")
        cur.execute(f"insert into save(scene, health, patrons, current_bul, type) values(-4, {player.health}, {player.bullets_amount}, {player.bullets}, '{player.attack_type}')")
        con.commit()
        next_sc = -5
        
        walls_group.empty()
        floor_list.empty()
        enemy_group.empty()
        objs_group.empty()
        objs_group.add(Object_pickup_types("sniper", 100, 600 , "pick"))
        objs_group.add(Object_pickup_types("down", 50 * len(level2[0]) - 100, 300 , "next"))
        
        map_obj.change2()
        map_obj.draw_map(walls_group)
        for o in walls_group:
            if o.typew == "wall": o.img = pygame.transform.scale(pygame.image.load("images/wall2.png"), (50, 50))
        for o in floor_list:
            o.img = pygame.transform.scale(pygame.image.load("images/floor2.png"), (50, 50))

        player.rect.x = 50
        player.rect.y = 1250
        scene = "c2"
    
    elif scene == -5:  # Переход на уровень 3
        cur.execute("DELETE FROM save")
        cur.execute(f"insert into save(scene, health, patrons, current_bul, type) values(-5, {player.health}, {player.bullets_amount}, {player.bullets}, '{player.attack_type}')")
        con.commit()
        next_sc = -6
        
        walls_group.empty()
        floor_list.empty()
        enemy_group.empty()
        objs_group.empty()
        objs_group.add(Object_pickup_types("down", len(level3[0]) * 50 - 100 , 32 * 50, "next"))
        
        map_obj.change3()
        map_obj.draw_map(walls_group)
        for o in walls_group:
            if o.typew == "wall": o.img = pygame.transform.scale(pygame.image.load("images/wall2.png"), (50, 50))
            if o.typew == "chair": o.img = pygame.transform.scale(pygame.image.load("images/chair2.png"), (50, 50))
            if o.typew == "decor": o.img = pygame.transform.scale(pygame.image.load("images/desk2.png"), (50, 50))
        for o in floor_list: 
            o.img = pygame.transform.scale(pygame.image.load("images/floor3.png"), (50, 50))

        player.rect.x = 100
        player.rect.y = 700
        scene = "c3"
    
    elif scene == -6:  # Переход на уровень с боссом
        cur.execute("DELETE FROM save")
        cur.execute(f"insert into save(scene, health, patrons, current_bul, type) values(-6, {player.health}, {player.bullets_amount}, {player.bullets}, '{player.attack_type}')")
        con.commit()
    
        walls_group.empty()
        floor_list.empty()
        enemy_group.empty()
        objs_group.empty()

        map_obj.change4()
        map_obj.draw_map(walls_group)

        boss_fight = True  # Исправлено: было boss_fight =- True

        player.rect.x = 100
        player.rect.y = 775

        for o in walls_group:
            if o.typew == "wall": o.img = pygame.transform.scale(pygame.image.load("images/wall3.png"), (50, 50))
        for o in floor_list: 
            o.img = pygame.transform.scale(pygame.image.load("images/floor4.jpg"), (50, 50))

        scene = 1

    clock.tick(30)
    pygame.display.flip()