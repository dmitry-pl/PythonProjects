import pygame
import sqlite3
from music_module import *
from button_saver import *
from player_class import *
from pathfinding import *
from cut_scene import *


pygame.init()
con = sqlite3.connect('save.db')
cur = con.cursor()

dis = pygame.display.set_mode((1500, 1000))
pygame.display.set_caption('PROJECT_WORLD.EXE')
pygame.display.set_icon(pygame.image.load('images/skull.png'))

contr_text = ["w a s d - перемещение", "стрелки - стрельба", "r - перезарядка", "space(зажать) - замедление времени", "e - взаимодейтвовать", "esc - пауза"]

#all images
#----------

back_menu = pygame.transform.scale(pygame.image.load('images/back_menu.png'), (1500, 1000))
death_menu = pygame.transform.scale(pygame.image.load('images/death_menu.png'), (1500, 1000))
time_stop = pygame.transform.scale(pygame.image.load('images/time_stop.png'), (1500, 1000))
time_stop.set_alpha(190)



#----------



clock = pygame.time.Clock()

game = True

scene = -1

music_menu()



time = False

saved = False

next_sc = -4

while game:
    dis.fill((200,200,200))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False

        if scene == 1:
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
                
            

            
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r and player.bullets < player.max_bullets:
                player.reload()

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

            if e.type == pygame.KEYDOWN and e.key == pygame.K_q:
                for en in enemy_group:
                    en.find_player = False

        if scene == "c1":
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                scene1.num += 1

        if scene == "c2":
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                scene2.num += 1

        if scene == "c3":
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                scene3.num += 1
 
                
        


        if e.type == pygame.MOUSEBUTTONDOWN and b_new_game.isOver(pygame.mouse.get_pos()) and scene == -1:
            scene = -2
            pygame.mixer.music.stop()
        if e.type == pygame.MOUSEBUTTONDOWN and b_continue2.isOver(pygame.mouse.get_pos()) and scene == -1:
            cur.execute("SELECT scene, health, patrons, current_bul, type FROM save")
            res = cur.fetchall()
            player.health = res[0][1]
            player.bullets_amount = res[0][2]
            player.bullets = res[0][3]
            player.attack_type = res[0][4]
            scene = res[0][ 0]
            pygame.mixer.music.stop()
            

        if e.type == pygame.MOUSEBUTTONDOWN and b_continue.isOver(pygame.mouse.get_pos()) and scene == -3:
            scene = 1
        if e.type == pygame.MOUSEBUTTONDOWN and b_about.isOver(pygame.mouse.get_pos()) and scene == -3:
            scene = "about"
        if e.type == pygame.MOUSEBUTTONDOWN and b_settings.isOver(pygame.mouse.get_pos()) and scene == -3:
            scene = "controls"
        if e.type == pygame.MOUSEBUTTONDOWN and b_back.isOver(pygame.mouse.get_pos()) and (scene == "about" or scene == "controls"):
            scene = -3
        if e.type == pygame.MOUSEBUTTONDOWN and b_menu.isOver(pygame.mouse.get_pos()) and (scene == -3):
            scene = -1
            music_menu()


        if e.type == pygame.MOUSEBUTTONDOWN and b_menu2.isOver(pygame.mouse.get_pos()) and (scene == -13):
            scene = -1
            music_menu()



        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            if scene == 1:
                scene = -3
                
            


    if scene == -1:

        dis.blit(back_menu, (0,0))
        b_new_game.draw(dis, pygame.mouse.get_pos())
        b_continue2.draw(dis, pygame.mouse.get_pos())

    if scene == -2:
        cur.execute("DELETE FROM save")
        
        cur.execute(f"insert into save(scene, health, patrons, current_bul, type) values(-2, {player.health}, {player.bullets_amount}, {player.bullets}, '{player.attack_type}')")
        con.commit()

        scene = "c1"
        map_obj.draw_map(walls_group)

        pygame.mixer.music.stop()

    if scene == -13:
        dis.blit(death_menu, (0,0))
        b_menu2.draw(dis, pygame.mouse.get_pos())

    
    


    if scene == -3:
        b_continue.draw(dis, pygame.mouse.get_pos())
        b_menu.draw(dis, pygame.mouse.get_pos())
        b_about.draw(dis, pygame.mouse.get_pos())
        b_settings.draw(dis, pygame.mouse.get_pos())

    if scene == "about":
        b_back.draw(dis, pygame.mouse.get_pos())

    if scene == "controls":
        b_back.draw(dis, pygame.mouse.get_pos())

        y = 140

        for t in contr_text:
            dis.blit(font.render(t, False, (0,0,0)), (40, y))
            y += 100


    if scene == 1:
        cam.update(player)
        floor_list.update(player, dis)
        

        if time:
            dis.blit(time_stop, (0,0))
            player.power -= 1
            if player.power < 1:
                time = False
                for e in enemy_group:
                    e.speed *= 3
        print(player.power)
        walls_group.update(player, dis)
        enemy_group.update(dis, player, walls_group)
        impacts.update(dis)
        scene =  player.update(dis, objs_group, walls_group, next_sc)

        
        objs_group.update(dis)
        

    if scene == "c1":
        scene = scene1.update(dis)
    if scene == "c2":
        scene = scene2.update(dis)
    if scene == "c3":
        scene = scene3.update(dis)

    if scene == -4:
        cur.execute("DELETE FROM save")
        cur.execute(f"insert into save(scene, health, patrons, current_bul, type) values(-4, {player.health}, {player.bullets_amount}, {player.bullets}, '{player.attack_type}')")
        con.commit()

        next_sc = -5
        
        
        walls_group.empty()
        floor_list.empty()
        enemy_group.empty()
        objs_group.empty()
        objs_group.add(Object_pickup_types("sniper", 100, 600 , "pick"))
        objs_group.add(Object_pickup_types("down", 50 * len(level2[0]) - 50, 300 , "next"))
            

        map_obj.change2()
        map_obj.draw_map(walls_group)
        #cam.state = pygame.Rect((0,0,map_obj.map_r[0]) * 50, len(map_obj.map_r) * 50)
        for o in walls_group:
            if o.typew == "wall":o.img = pygame.transform.scale(pygame.image.load("images/wall2.png"), (50, 50))
        for o in floor_list:
            o.img = pygame.transform.scale(pygame.image.load("images/floor2.png"), (50, 50))

        player.rect.x = 50
        player.rect.y = 1250
        scene = "c2"
        print(walls_group)

    if scene == -5:
        cur.execute("DELETE FROM save")
        cur.execute(f"insert into save(scene, health, patrons, current_bul, type) values(-5, {player.health}, {player.bullets_amount}, {player.bullets}, '{player.attack_type}')")
        con.commit()


        next_sc = -5
        
        
        walls_group.empty()
        floor_list.empty()
        enemy_group.empty()
        objs_group.empty()
        
        map_obj.change3()
        map_obj.draw_map(walls_group)

        for o in walls_group:
            if o.typew == "wall":o.img = pygame.transform.scale(pygame.image.load("images/wall2.png"), (50, 50))
            if o.typew == "chair":o.img = pygame.transform.scale(pygame.image.load("images/chair2.png"), (50, 50))
            if o.typew == "decor":o.img = pygame.transform.scale(pygame.image.load("images/desk2.png"), (50, 50))
        for o in floor_list: o.img = pygame.transform.scale(pygame.image.load("images/floor3.png"), (50, 50))

        player.rect.x = 100
        player.rect.y = 700
        scene = "c3"
    
        
    
        

        

        
        


     
        

    clock.tick(30)
    pygame.display.flip()