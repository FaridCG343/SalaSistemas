from helpers.VAO import VAO
from helpers.Texture import Texture


class Mesh:
    def __init__(self, app):
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app.ctx)
        self.texture_array = {
            'wood-floor': [
                self.texture.textures['wood-floor'],
                self.texture.textures['wood-floor'],
                self.texture.textures['wood-floor'],
                self.texture.textures['wood-floor'],
                self.texture.textures['wood-floor'],
                self.texture.textures['wood-floor']
            ]
        }

    def destroy(self):
        self.vao.destroy()
        self.texture.destroy()
