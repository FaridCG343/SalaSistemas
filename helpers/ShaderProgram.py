class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {
            'default': self.get_shader_program('default_texture'),
            'axis': self.get_shader_program('axis'),
            'default_color': self.get_shader_program('default_color'),
            'light_cube': self.get_shader_program('light_cube'),
        }

    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert', 'r') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag', 'r') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def destroy(self):
        [program.release() for program in self.programs.values()]
