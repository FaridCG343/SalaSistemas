from helpers.VBO import VBO
from helpers.ShaderProgram import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.shader_program = ShaderProgram(ctx)
        self.vaos = {
            'cube': self.get_vao(program=self.shader_program.programs['default'],
                                 vbo=self.vbo.vbos['cube']),
            'axis': self.get_vao(program=self.shader_program.programs['axis'],
                                 vbo=self.vbo.vbos['axis']),
            'cube_color': self.get_vao(program=self.shader_program.programs['default_color'],
                                       vbo=self.vbo.vbos['cube_color']),
            'light_cube': self.get_vao(program=self.shader_program.programs['light_cube'],
                                       vbo=self.vbo.vbos['cube_color'])
        }

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attrib)])
        return vao

    def destroy(self):
        [vao.release() for vao in self.vaos.values()]
        self.vbo.destroy()
        self.shader_program.destroy()
