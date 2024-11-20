import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Definir los vértices, aristas y caras de un cubo
vertices = [
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

surfaces = [
    (0, 1, 2, 3),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
    (2, 3, 7, 6),
    (0, 3, 7, 4),
    (1, 2, 6, 5)
]

colors = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 1]
]


# Función para dibujar el cubo
def draw_cube():
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        glColor3fv(colors[i])
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    glColor3f(0, 0, 0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


# Configuración inicial de OpenGL
def init_opengl():
    glClearColor(.75, .75, .75, 1)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)


# Función principal
def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)

    init_opengl()

    glTranslatef(0.0, 0.0, -5)

    # Variables para rotación con el mouse
    mouse_sensitivity = 0.2
    rotation_x = 0
    rotation_y = 0
    last_mouse_pos = pygame.mouse.get_pos()
    rotating = False  # Indica si el botón del ratón está presionado

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Detectar cuando se presiona el botón del ratón
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo
                    rotating = True
                    last_mouse_pos = pygame.mouse.get_pos()

            # Detectar cuando se suelta el botón del ratón
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Botón izquierdo
                    rotating = False

        # Si el botón del ratón está presionado, rotar
        if rotating:
            current_mouse_pos = pygame.mouse.get_pos()
            dx = current_mouse_pos[0] - last_mouse_pos[0]
            dy = current_mouse_pos[1] - last_mouse_pos[1]
            last_mouse_pos = current_mouse_pos

            # Actualizar las rotaciones en función del movimiento del ratón
            rotation_x += dy * mouse_sensitivity
            rotation_y += dx * mouse_sensitivity

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5)  # Volver a posicionar la cámara
        glRotatef(rotation_x, 1, 0, 0)  # Rotar en el eje X
        glRotatef(rotation_y, 0, 1, 0)  # Rotar en el eje Y

        draw_cube()  # Dibujar el cubo

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    main()
