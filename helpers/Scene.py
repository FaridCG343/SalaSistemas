from models.Model import *
from models.ComposedModels import *


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()


    def add_object(self, obj):
        self.objects.append(obj)

    def add_objects(self, objs):
        self.objects.extend(objs)

    def load(self):
        app = self.app
        add = self.add_object
        add_objects = self.add_objects
        add(Axis(app))

        # get the position of the light to create a cube in that position
        add(LightCube(app, pos=app.light.position, scale=(1, 1, 1)))

        # add_objects(Table(app, scale=(1.5, 1, 1.5)).get_objects())  # 7.5, 0.5, 4.5
        # add_objects(Monitor(app, pos=(0, 4.3, 0)).get_objects())

        # 5 x 5
        # range inico, fin, step
        for x in range(-60, 80, 20):
            for z in range(-30, 18, 12):
                add_objects(Table(app, scale=(1.5, 1, 1.5), pos=(x, 0, z)).get_objects())
                add_objects(Monitor(app, pos=(x, 4.3, z)).get_objects())

    def render(self):
        for obj in self.objects:
            obj.render()
