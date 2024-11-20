from models.Model import *


class BaseComposedModel:
    def __init__(self, app, scale=(1, 1, 1), pos=(0, 0, 0), rot=(0, 0, 0)):
        self.app = app
        self.scale = scale
        self.pos = pos
        self.rot = rot
        self.objects = []

    def get_objects(self):
        return self.objects


class Table(BaseComposedModel):
    def __init__(self, app, scale=(1, 1, 1), pos=(0, 0, 0)):
        super().__init__(app, scale, pos)

        # Parámetros de la base
        base_scale = (5, 0.5, 3)
        base_pos = (0, 0, 0)
        actual_base_scale = (base_scale[0] * scale[0], base_scale[1], base_scale[2] * scale[2])
        actual_base_pos = tuple(b + p for b, p in zip(base_pos, pos))

        # Creación del cubo de la base
        base_cube = Cube(app, text_id='marble', scale=actual_base_scale, pos=actual_base_pos)

        # Parámetros de las patas
        leg_scale = (0.5, 2.5, 2)
        leg_pos = (4.5, -2.5, 0)
        leg_pos2 = (-4.5, -2.5, 0)

        # Escalar las patas en Y solamente
        actual_leg_scale = (leg_scale[0], leg_scale[1] * scale[1], leg_scale[2] * scale[2])

        # Ajustar la posición de las patas en X según la escala
        actual_leg_pos = (pos[0] + (leg_pos[0] * scale[0]) + 0.5 * (scale[0] - 1), (leg_pos[1] * scale[1]) + pos[1],
                          leg_pos[2] + pos[2])
        actual_leg_pos2 = (pos[0] + (leg_pos2[0] * scale[0]) - 0.5 * (scale[0] - 1), (leg_pos2[1] * scale[1]) + pos[1],
                           leg_pos2[2] + pos[2])

        # Creación de las patas
        leg_cube = Cube(app, text_id='rubber', scale=actual_leg_scale, pos=actual_leg_pos)
        leg_cube2 = Cube(app, text_id='rubber', scale=actual_leg_scale, pos=actual_leg_pos2)

        # Añadir los objetos a la lista
        self.objects.extend([base_cube, leg_cube, leg_cube2])


class Monitor(BaseComposedModel):
    def __init__(self, app, pos=(0, 0, 0)):
        super().__init__(app, pos=pos)

        # Parámetros de la pantalla del monitor
        screen_scale = (4, 2.5, 0.2)  # Ancho, alto, profundidad de la pantalla

        # Parámetros de la pantalla frontal
        screen_front_scale = (4, 2.5, 0.1)
        screen_front_pos = (0, 0, 0.15)
        actual_screen_front_pos = tuple(s + p for s, p in zip(screen_front_pos, pos))

        # Parámetros de la base
        base_scale = (0.3, 1, 0.1)
        base_pos = (0, -2.5, -0.12)
        actual_base_pos = tuple(b + p for b, p in zip(base_pos, pos))

        base2_scale = (2.5, 0.1, 1)
        base2_pos = (0, -3.5, 0)
        actual_base2_pos = tuple(b + p for b, p in zip(base2_pos, pos))


        # Creación del cubo de la pantalla del monitor
        screen_cube = Cube(app, text_id='rubber', scale=screen_scale, pos=pos)
        screen_front_cube = Cube(app, text_id='windows', scale=screen_front_scale, pos=actual_screen_front_pos)
        base_cube = Cube(app, text_id='rubber', scale=base_scale, pos=actual_base_pos)
        base_cube2 = Cube(app, text_id='rubber', scale=base2_scale, pos=actual_base2_pos)

        # Añadir los objetos a la lista
        self.objects.extend([screen_cube, screen_front_cube, base_cube, base_cube2])


