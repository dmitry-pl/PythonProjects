import pygame

class Scenes():
    def __init__(self, text, next, cur):
        self.text = text
        self.num = 0
        self.font = pygame.font.Font('fonts/Трафарет ГОСТ 14192- 96.ttf', 50)
        self.next_scene = next
        self.current = cur


    def update(self, dis):
        if self.num == len(self.text):
            return self.next_scene
        dis.blit(self.font.render(self.text[self.num], False, (0, 0, 0)), (40, 40))
        return self.current
        



scene1 = Scenes(["2100 год н.э", ":Я на месте", "?:Отлично. Теперь найди вход в бункер.", "?:Где то там находится главный сервер, который управляет этими зомби"], 1, "c1")
scene2 = Scenes(["?:Отлично, ты нашёл вход.", ":Подожди, ты кто? Откуда ты говоришь?", "Главный сервер(?):Чёрт, один выбился из под контроля", ":Похоже, это и есть главный сервер"], 1, "c2")
scene3 = Scenes([":Ещё один этаж? Похоже, в этом здании раньше был офис", ":Я слышу странные звуки... Похоже, сервер уже близко"], 1, "c3")