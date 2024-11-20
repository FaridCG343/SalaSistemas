import glm
import moderngl as mgl

M_TRANSLATE = 1
M_ROTATE = 2
M_SCALE = 3


class BaseModel:
    def __init__(self, app, vao_name, text_id, pos=(0, 0, 0), scale=(1, 1, 1), rot=(0, 0, 0),
                 transformation_order=None):
        if transformation_order is None:
            self.transformation_order = [M_TRANSLATE, M_ROTATE, M_SCALE]
        else:
            self.transformation_order = transformation_order
        self.app = app
        self.pos = pos
        self.scale = scale
        self.rot = glm.vec3([glm.radians(r) for r in rot])
        self.m_model = self.get_model_matrix()
        self.text_id = text_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = app.camera

    def update(self):
        ...

    def get_model_matrix(self):
        m_model = glm.mat4(1)
        # aplicar transformaciones en el orden especificado
        for t in self.transformation_order:
            if t == M_TRANSLATE:
                m_model = glm.translate(m_model, glm.vec3(self.pos))
            elif t == M_ROTATE:
                m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
                m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
                m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
            elif t == M_SCALE:
                m_model = glm.scale(m_model, glm.vec3(self.scale))
        return m_model

    def render(self):
        self.update()
        self.vao.render()


class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', text_id='wood-floor', pos=(0, 0, 0), scale=(1, 1, 1), rot=(0, 0, 0), transformation_order=None):
        super().__init__(app, vao_name, text_id, pos, scale, rot, transformation_order)
        self.texture = None
        self.ctx = app.ctx
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['model'].write(self.m_model)
        self.program['view'].write(self.app.camera.m_view)
        self.program['camPos'].write(self.app.camera.position)

    def on_init(self):
        # luz
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)
        # textura
        self.program['u_texture'] = 0
        self.texture = self.app.mesh.texture.textures[self.text_id]
        # mvp (model view projection)
        self.program['projection'].write(self.app.camera.m_projection)
        self.program['view'].write(self.app.camera.m_view)
        self.program['model'].write(self.m_model)


class CubeColor(BaseModel):
    def __init__(self, app, vao_name='cube_color', color=(1, 1, 1), pos=(0, 0, 0), scale=(1, 1, 1), rot=(0, 0, 0),
                 transformation_order=None):
        super().__init__(app, vao_name, None, pos, scale, rot, transformation_order)
        self.texture = None
        self.ctx = app.ctx
        self.on_init()

    def update(self):
        self.program['model'].write(self.m_model)
        self.program['view'].write(self.app.camera.m_view)
        self.program['camPos'].write(self.app.camera.position)

    def on_init(self):
        # luz
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)
        # mvp (model view projection)
        self.program['projection'].write(self.app.camera.m_projection)
        self.program['view'].write(self.app.camera.m_view)
        self.program['model'].write(self.m_model)


class LightCube(BaseModel):
    def __init__(self, app, vao_name='light_cube', text_id=None, pos=(0, 0, 0), scale=(1, 1, 1), rot=(0, 0, 0),
                 transformation_order=None):
        super().__init__(app, vao_name, text_id, pos, scale, rot, transformation_order)
        self.texture = None
        self.ctx = app.ctx
        self.on_init()

    def update(self):
        self.program['model'].write(self.m_model)
        self.program['view'].write(self.app.camera.m_view)

    def on_init(self):
        # mvp (model view projection)
        self.program['projection'].write(self.app.camera.m_projection)
        self.program['view'].write(self.app.camera.m_view)
        self.program['model'].write(self.m_model)


class Axis(BaseModel):
    def __init__(self, app, vao_name='axis', text_id='axis'):
        super().__init__(app, vao_name, text_id)
        self.texture = None
        self.ctx = app.ctx
        self.on_init()

    def update(self):
        self.program['model'].write(self.m_model)
        self.program['view'].write(self.app.camera.m_view)
        self.program['projection'].write(self.app.camera.m_projection)

    def on_init(self):
        # mvp (model view projection)
        self.program['projection'].write(self.app.camera.m_projection)
        self.program['view'].write(self.app.camera.m_view)
        self.program['model'].write(self.m_model)

    def render(self):
        self.update()
        self.vao.render(mgl.LINES)
