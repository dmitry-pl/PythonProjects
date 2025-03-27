import pygame

pygame.init()

shot = pygame.mixer.Sound("sound/shoot.mp3")
kill = pygame.mixer.Sound("sound/kill_sound.mp3")
pickups = pygame.mixer.Sound("sound/pickup.mp3")

def music_menu():
    pygame.mixer.music.load('sound/menu_music.mp3')
    pygame.mixer.music.play(-1)

def shoot():
    pygame.mixer.Sound.play(shot)

def killf():
    pygame.mixer.Sound.play(kill)

def pickup():
    pygame.mixer.Sound.play(pickups)