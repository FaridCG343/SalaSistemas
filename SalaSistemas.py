import glm
import moderngl as mgl
import sys

import numpy as np
import pygame as pg
from helpers.Mesh import Mesh
from helpers.Scene import Scene
from helpers.Camera import Camera
from helpers.Light import Light


class SalaSistemas:
    def __init__(self, window_size=(800, 600)):
        # Inicializar Pygame
        pg.init()

        # tamaño de la ventana
        self.window_size = window_size

        # setear los atributos de opengl
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        # configuraciones del mouse
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        # Crear el contexto de opengl
        pg.display.set_mode(self.window_size, flags=pg.DOUBLEBUF | pg.OPENGL)
        self.ctx = mgl.create_context()
        self.ctx.enable(mgl.DEPTH_TEST | mgl.CULL_FACE)

        # Crear un objeto para ayudar con el tiempo
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        # Crear la luz
        self.light = Light(position=(0, 7, 0))

        # Crear la camara
        self.camera = Camera(self)

        # mesh
        self.mesh = Mesh(self)

        # Escenario
        self.scene = Scene(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        self.ctx.clear(0.1, 0.1, 0.1)

        self.scene.render()

        pg.display.flip()

    def get_time(self):
        self.time += self.clock.get_time() / 1000

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)


if __name__ == '__main__':
    app = SalaSistemas()
    app.run()
