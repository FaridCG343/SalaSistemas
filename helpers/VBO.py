from __future__ import annotations

import numpy as np


class VBO:
    def __init__(self, ctx):
        self.vbos = {
            'cube': CubeVBO(ctx),
            'axis': AxisVBO(ctx),
            'cube_color': CubeColorVBO(ctx)
        }

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]


class BaseVBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str | None = None
        self.attrib: list | None = None

    def get_vertex_data(self): ...

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def destroy(self):
        self.vbo.release()


class CubeVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attrib = ['in_texcoord_0', 'in_normal', 'in_position']

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)
        texture_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
        texture_coords_indices = [(0, 2, 3), (0, 1, 2),
                                  (0, 2, 3), (0, 1, 2),
                                  (0, 1, 2), (2, 3, 0),
                                  (2, 3, 0), (2, 0, 1),
                                  (0, 2, 3), (0, 1, 2),
                                  (3, 1, 2), (3, 0, 1)]
        tex_coord_data = self.get_data(texture_coords, texture_coords_indices)
        normals = [
            (0, 0, 1) * 6,
            (1, 0, 0) * 6,
            (0, 0, -1) * 6,
            (-1, 0, 0) * 6,
            (0, 1, 0) * 6,
            (0, -1, 0) * 6
        ]
        normals = np.array(normals, dtype='f4').reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data



class CubeColorVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f 3f'
        self.attrib = ['in_normal', 'in_position']

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)

        normals = [
            (0, 0, 1) * 6,
            (1, 0, 0) * 6,
            (0, 0, -1) * 6,
            (-1, 0, 0) * 6,
            (0, 1, 0) * 6,
            (0, -1, 0) * 6
        ]
        normals = np.array(normals, dtype='f4').reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        return vertex_data


class AxisVBO(BaseVBO):
    def __init__(self, ctx):
        self.grid_size = 50
        super().__init__(ctx)
        self.format = '3f 3f'
        self.attrib = ['in_vert', 'in_color']

    def get_vertex_data(self):
        # Tamaño de la cuadrícula (de -10 a 10 en X y Z)
        grid_size = self.grid_size
        color_axis = (0.25, 0.25, 0.25)
        color_origin_x_pos = (1.0, 0.0, 0.0)  # Rojo
        color_origin_y_pos = (0.0, 1.0, 0.0)  # Verde
        color_origin_z_pos = (0.0, 0.0, 1.0)  # Azul
        color_origin_x_neg = (1.0, 1.0, 0.0)  # Amarillo
        color_origin_y_neg = (0.0, 1.0, 1.0)  # Cyan
        color_origin_z_neg = (1.0, 0.0, 1.0)  # Magenta

        vertices_grid = []

        # Generar las líneas horizontales (paralelas al eje X), excluyendo la del origen

        for z in range(-grid_size, grid_size + 1):
            if z != 0:  # Excluir la línea del origen (eje Z)
                vertices_grid.extend([
                    -grid_size, 0.0, z, *color_axis,
                    grid_size, 0.0, z, *color_axis  # a (grid_size, z)
                ])
            else:
                vertices_grid.extend([
                    0.0, 0.0, z, *color_origin_z_neg,
                    0.0, 0.0, -grid_size, *color_origin_z_neg  # a (0, -grid_size)
                ])
                vertices_grid.extend([
                    0.0, 0.0, z, *color_origin_z_pos,
                    0.0, 0.0, grid_size, *color_origin_z_pos  # a (0, grid_size)
                ])

        # Generar las líneas verticales (paralelas al eje Z), excluyendo la del origen
        for x in range(-grid_size, grid_size + 1):
            if x != 0:  # Excluir la línea del origen (eje X)
                vertices_grid.extend([
                    x, 0.0, -grid_size, *color_axis,
                    x, 0.0, grid_size, *color_axis  # a (x, grid_size)
                ])
            else:
                vertices_grid.extend([
                    x, 0.0, 0.0, *color_origin_x_neg,
                    -grid_size, 0.0, 0.0, *color_origin_x_neg  # a (-grid_size, 0)
                ])
                vertices_grid.extend([
                    x, 0.0, 0.0, *color_origin_x_pos,
                    grid_size, 0.0, 0.0, *color_origin_x_pos  # a (grid_size, 0)
                ])

        vertices_grid.extend([
            0.0, 0.0, 0.0, *color_origin_y_neg,
            0.0, -grid_size, 0.0, *color_origin_y_neg  # a (0, -grid_size)
        ])
        vertices_grid.extend([
            0.0, 0.0, 0.0, *color_origin_y_pos,
            0.0, grid_size, 0.0, *color_origin_y_pos  # a (0, grid_size)
        ])

        # Convertir los vértices a un arreglo de NumPy
        vertices_grid = np.array(vertices_grid, dtype='f4')
        return vertices_grid.tobytes()
