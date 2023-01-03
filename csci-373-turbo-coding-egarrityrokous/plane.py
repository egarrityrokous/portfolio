import numpy as np
import os
import pygame as pg


class Message:

    def __init__(self, x, y, msg, color, font_size):
        self.x, self.y = x, y
        self.color = color
        self.font_size = font_size
        self.move_divisor = 10
        self.move_queue = []
        self.myfont = pg.font.SysFont("monospace", self.font_size)
        self.text_box = self.myfont.render(msg, 1, self.color)
        self.text = msg

    def reset_message(self, msg):
        self.text_box = self.myfont.render(msg, 1, self.color)
        self.text = msg

    def reset_color(self, color):
        self.color = color
        self.text_box = self.myfont.render(self.text, 1, self.color)

    def is_stationary(self):
        return len(self.move_queue) == 0

    def move(self, delta_x, delta_y):
        step_size = (delta_x / self.move_divisor, delta_y / self.move_divisor)
        self.move_queue += [step_size] * self.move_divisor

    def get_location(self):
        return self.x, self.y

    def size(self):
        return self.text_box.get_rect().size

    def get_object(self):
        return self.text_box

    def notify(self, event):
        pass

    def update(self):
        if len(self.move_queue) > 0:
            (delta_x, delta_y), self.move_queue = self.move_queue[0], self.move_queue[1:]
            self.x, self.y = self.x + delta_x, self.y + delta_y


class CartesianPlane:
    def __init__(self, x_max, y_max, screen_width, screen_height,
                 bg_color=(47, 49, 51),
                 grid_color=(27, 29, 31)):
        self.screen = pg.display.set_mode((screen_width, screen_height), pg.SCALED)
        self.background = pg.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(bg_color)
        self.screen_width, self.screen_height = self.screen.get_size()
        self.x_max = x_max
        self.y_max = y_max
        self.x_pixel_increment = self.screen_width // self.x_max
        self.y_pixel_increment = self.screen_height // self.y_max
        for y in range(self.y_pixel_increment, self.screen_height, self.y_pixel_increment):
            pg.draw.aaline(self.background, grid_color, (0, y), (self.screen_width, y))
        for x in range(self.x_pixel_increment, self.screen_width, self.x_pixel_increment):
            pg.draw.aaline(self.background, grid_color, (x, 0), (x, self.screen_height))
        self.screen.blit(self.background, (0, 0))
        pg.display.flip()
        self.screen = pg.display.get_surface()
        self.objects = []

    def clear(self):
        self.objects = []

    def put(self, object):
        self.objects.append(object)

    def refresh(self):
        self.screen.blit(self.background, (0, 0))
        for object in self.objects:
            object.update()
            x, y = object.get_location()
            new_x, new_y = self.translate_coordinates(x, y)
            width, height = object.size()
            ul_x, ul_y = new_x - width // 2, new_y - height // 2
            self.screen.blit(object.get_object(), (ul_x, ul_y))
        pg.display.flip()

    def notify(self, event):
        for object in self.objects:
            object.notify(event)

    def in_bounds(self, x, y):
        return 0 <= x <= self.x_max, 0 <= y <= self.y_max

    def translate_coordinates(self, x, y):
        return (x * self.x_pixel_increment,
                self.screen_height - (y * self.y_pixel_increment))

