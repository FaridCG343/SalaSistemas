import pygame as pg
import moderngl as mgl


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {
            'wood-floor': self.get_texture('textures/wood-floor.jpg'),
            'tile-wall': self.get_texture('textures/tiles-wall.jpg'),
            'space': self.get_texture('textures/space.jpg'),
            'windows': self.get_texture('textures/windows.jpg'),
            'marble': self.get_texture('textures/marble.jpg'),
            'rubber': self.get_texture('textures/rubber.jpg'),
        }

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, False, True)
        texture = self.ctx.texture(size=texture.get_size(), components=3, data=pg.image.tostring(texture, 'RGB'))

        # Mipmaps (los mipmaps son texturas de menor resolución que la original)
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()

        # AF (Anisotropic Filtering) (mejora la calidad de las texturas)
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        [texture.release() for texture in self.textures.values()]
