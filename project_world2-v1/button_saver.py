import pygame
from button_class import Button

pygame.init()

b_new_game = Button(40, 40, 300, 86, 'images/buttons/new_game_b.png', "images/buttons/new_game_b_sel.png")
b_continue = Button(40, 40, 300, 86, 'images/buttons/continue_b.png', "images/buttons/continue_b_sel.png")
b_menu = Button(40, 140, 300, 86, 'images/buttons/menu_b.png', "images/buttons/menu_b_sel.png")
b_menu2 = Button(40, 40, 300, 86, 'images/buttons/menu_b.png', "images/buttons/menu_b_sel.png")
b_about = Button(40, 240, 300, 86, 'images/buttons/about_b.png', "images/buttons/about_b_sel.png")
b_back = Button(40, 40, 300, 86, 'images/buttons/back_b.png', "images/buttons/back_b_sel.png")
b_settings = Button(40, 340, 300, 86, 'images/buttons/settings_b.png', "images/buttons/settings_b_sel.png")
b_continue2 = Button(40, 140, 300, 86, 'images/buttons/continue_b.png', "images/buttons/continue_b_sel.png")