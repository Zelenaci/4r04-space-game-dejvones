#!/usr/bin/env python3
# Soubor:  kameny.py
# Datum:   06.11.2018 10:01
# Autor:   Marek Nožka, nozka <@t> spseol <d.t> cz
# Licence: GNU/GPL
############################################################################
import pyglet
import random
from math import sin, cos, radians, pi
from pyglet.window import key


window = pyglet.window.Window(1000, 800)
batch = pyglet.graphics.Batch()   # pro optimalizované vyreslování objektů
klavesy = set ()

class Stone(object):

    def __init__(self, x=None, y=None, direction=None, speed=None, rspeed=None):
        # nečtu obrázek
        num = random.choice(range(0, 20))
        self.image = pyglet.image.load('meteors/{}.png'.format(num))
        # střed otáčení dám na střed obrázku
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2
        # z obrázku vytvořím sprite
        self.sprite = pyglet.sprite.Sprite(self.image, batch=batch)
        # pokud není atribut zadán vytvořím ho náhodně
        self.x = x if x is not None else random.randint(0,1000)
        self.y = y if y is not None else random.randint(200,800)
        # musím správně nastavit polohu sprite
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.direction = direction \
            if direction is not None else random.randint(0, 359)
        # rychlost pohybu
        self.speed = speed \
            if speed is not None else random.randint(80, 120)
        # rychlost otáčení
        self.rspeed = rspeed \
            if rspeed is not None else random.randint(-100, 100)
        self.rotation = 0

    def tick(self, dt):
        self.bounce()
        # do promenne dt se uloží doba od posledního tiknutí
        self.x += dt * self.speed * cos(pi / 2 - radians(self.direction))
        self.sprite.x = self.x
        self.y += dt * self.speed * sin(pi / 2 - radians(self.direction))
        self.sprite.y = self.y
        self.sprite.rotation += 0.01 * self.rspeed
    def bounce(self):
        # vzdálenost okraje a středu
        rozmer = min(self.image.width, self.image.height)/2
        if self.x + rozmer >= window.width:
            self.direction = random.randint(190, 350)
            return
        if self.x - rozmer <= 0:
            self.direction = random.randint(10, 170)
            return
        if self.y + rozmer >= window.height:
            self.direction = random.randint(100, 260)
            return
        if self.y - rozmer <= 0:
            self.direction = random.randint(-80, 80)
            return

class Raketa(object):
        def __init__(self, x=None, y=None, direction=None, speed=None, rspeed=None):
            global smer
            global rychlost
            self.image = pyglet.image.load('playerShip1_red.png')
            # střed otáčení dám na střed obrázku
            self.image.anchor_x = self.image.width // 2
            self.image.anchor_y = self.image.height // 2
            # z obrázku vytvořím sprite
            self.sprite = pyglet.sprite.Sprite(self.image, batch=batch)
            self.x = 500
            self.y = 50
            self.rotation = 0
            self.sprite.x = self.x
            self.sprite.y = self.y       
            self.rychlost = 0
            self.uhel = 0  
            
        def tick(self, dt):
            self.bounce()
            rozmer = min(self.image.width, self.image.height)/2
            for sym in klavesy:   
                if sym == key.RIGHT:
                    self.rotation += 10
                    self.uhel += 10
                elif sym == key.LEFT:
                    self.rotation -= 10
                    self.uhel -= 10
                elif sym == key.UP:
                    self.rychlost = 200
                    self.x += dt * self.rychlost * cos(pi / 2 - radians(self.uhel))
                    if self.x + rozmer >= window.width or self.x - rozmer <= 0:
                        pass
                    else:    
                        self.sprite.x = self.x
                    self.y += dt * self.rychlost * sin(pi / 2 - radians(self.uhel))
                    if self.y + rozmer >= window.height or self.y - rozmer <= 0:
                        pass
                    else:
                        self.sprite.y = self.y   
                elif sym == key.DOWN:
                    self.rychlost = 200
                    self.x += dt * self.rychlost * -cos(pi / 2 - radians(self.uhel))
                    if self.x + rozmer >= window.width or self.x - rozmer <= 0:
                        pass
                    else:    
                        self.sprite.x = self.x
                    self.y += dt * self.rychlost * -sin(pi / 2 - radians(self.uhel))
                    if self.y + rozmer >= window.height or self.y - rozmer <= 0:
                        pass
                    else:
                        self.sprite.y = self.y 
            self.sprite.rotation = self.rotation

        def bounce(self):
            rozmer = min(self.image.width, self.image.height)/2
            if self.x + rozmer >= window.width:
                self.rychlost = 0
                return
            if self.x - rozmer <= 0:
                self.rychlost = 0
                return
            if self.y + rozmer >= window.height:
                self.rychlost = 0
                return
            if self.y - rozmer <= 0:
                self.rychlost = 0
                return

stones = []
for i in range(30):
    stone = Stone()
    pyglet.clock.schedule_interval(stone.tick, 1 / 60)
    stones.append(stone)

raketa = Raketa()
pyglet.clock.schedule_interval(raketa.tick, 1 / 60)

@window.event
def on_draw():
    window.clear()
    batch.draw()
    
@window.event
def on_key_press(sym, mod):
    global klavesy
    klavesy.add(sym)
    
@window.event
def on_key_release(sym, mod):
    global klavesy
    klavesy.remove(sym) 


pyglet.app.run()
