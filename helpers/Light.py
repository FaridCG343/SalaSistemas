import glm


class Light:
    def __init__(self, position=(3, 3, -3), color=(1, 1, 1)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)

        # Intensidades
        self.Ia = 0.2 * self.color  # Intensidad ambiental
        self.Id = 0.8 * self.color  # Intensidad difusa
        self.Is = 0.5 * self.color  # Intensidad especular
