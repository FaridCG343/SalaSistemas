import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


# Función para dibujar un triángulo
def draw_triangle():
    glBegin(GL_TRIANGLES)  # Iniciar el dibujado de triángulos
    glColor3f(1, 0, 0)  # Color rojo
    glVertex3f(0, 1, 0)  # Vértice superior
    glColor3f(0, 1, 0)  # Color verde
    glVertex3f(-1, -1, 0)  # Vértice inferior izquierdo
    glColor3f(0, 0, 1)  # Color azul
    glVertex3f(1, -1, 0)  # Vértice inferior derecho
    glEnd()  # Finalizar el dibujado


# Configuración inicial de OpenGL
def init_opengl():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Color de fondo (negro)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)  # Habilitar test de profundidad
    glDepthFunc(GL_LEQUAL)  # Tipo de test de profundidad
    glShadeModel(GL_SMOOTH)  # Suavizado de colores
    glMatrixMode(GL_PROJECTION)  # Configuración de la matriz de proyección
    glLoadIdentity()
    gluPerspective(45, (800 / 600), 0.1, 50.0)  # Perspectiva
    glMatrixMode(GL_MODELVIEW)


# Función principal
def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)

    init_opengl()  # Inicializar OpenGL

    # Configurar la posición inicial de la cámara
    glTranslatef(0.0, 0.0, -5)

    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpiar pantalla y buffer de profundidad

        draw_triangle()  # Dibujar el triángulo

        pygame.display.flip()  # Actualizar la pantalla
        pygame.time.wait(10)  # Pequeño retardo para evitar sobrecargar la CPU

    pygame.quit()


if __name__ == "__main__":
    main()
