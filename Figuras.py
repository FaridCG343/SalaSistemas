import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QSpinBox, \
    QColorDialog, QPushButton
from PyQt5.QtGui import QColor
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from OpenGL.GLUT import *


class OpenGLWidget(QGLWidget):
    def __init__(self):
        super(OpenGLWidget, self).__init__()
        self.figure = None
        self.width = 50
        self.height = 50
        self.container_width = 800
        self.container_height = 600
        self.area = 0
        self.perimeter = 0
        self.color = (0.0, 0.0, 0.0)
        self.scale = 20  # Escala para los ejes y escalado de figuras

    def set_figure(self, figure, width, height, color):
        self.figure = figure
        self.width = width
        self.height = height
        self.calculate_area_perimeter()
        self.width = width * self.scale
        self.height = height * self.scale
        self.color = color
        self.update()  # Llamar a update() para volver a renderizar la figura

    def resizeGL(self, width, height):
        self.container_width = width
        self.container_height = height
        # Este método se llama automáticamente cuando la ventana cambia de tamaño
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Ajustar glOrtho para que el origen esté en el centro del contenedor
        glOrtho(-width / 2, width / 2, -height / 2, height / 2, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(1, 1, 1, 1)
        glLoadIdentity()

        # Dibujar los ejes cartesianos
        self.draw_axes()

        # Resaltar el origen
        self.draw_origin()

        # Dibujar las figuras según la selección
        glColor3f(self.color[0], self.color[1], self.color[2])
        if self.figure == "Círculo":
            self.draw_circle(0, 0, self.width)
        elif self.figure == "Triángulo":
            self.draw_triangle(0, 0, self.width, self.height)
        elif self.figure == "Cuadrado":
            self.draw_rectangle(-self.width / 2, -self.width / 2, self.width, self.width)
        elif self.figure == "Rectángulo":
            self.draw_rectangle(-self.width / 2, -self.height / 2, self.width, self.height)

        # Dibujar el área y el perímetro
        glColor(0.0, 0.0, 0.0)
        self.renderText(-self.container_width // 2 + 10, self.container_height // 2 - 30, 0,
                        f"Área: {self.area:.2f}")
        self.renderText(-self.container_width // 2 + 10, self.container_height // 2 - 60, 0,
                        f"Perímetro: {self.perimeter:.2f}")

    def draw_axes(self):
        """Dibuja los ejes X e Y del plano cartesiano"""
        glColor3f(0.0, 0.0, 0.0)  # Color negro para los ejes
        glLineWidth(2)

        # Eje X
        glBegin(GL_LINES)
        glVertex2f(-self.container_width // 2, 0)
        glVertex2f(self.container_width // 2, 0)
        glEnd()

        # Eje Y
        glBegin(GL_LINES)
        glVertex2f(0, -self.container_height // 2)
        glVertex2f(0, self.container_height // 2)
        glEnd()

        # Dibujar marcas en los ejes
        self.draw_axis_marks()

    def draw_axis_marks(self):
        """Dibuja marcas pequeñas en los ejes X e Y"""
        glColor3f(0.0, 0.0, 0.0)  # Color negro para las marcas
        glLineWidth(1)

        # Marcas en el eje X
        for x in range(0, self.container_width // 2, self.scale):
            glBegin(GL_LINES)
            glVertex2f(x, -5)
            glVertex2f(x, 5)
            glEnd()
            glBegin(GL_LINES)
            glVertex2f(-x, -5)
            glVertex2f(-x, 5)
            glEnd()

        # Marcas en el eje Y
        for y in range(0, self.container_height // 2, self.scale):
            glBegin(GL_LINES)
            glVertex2f(-5, y)
            glVertex2f(5, y)
            glEnd()
            glBegin(GL_LINES)
            glVertex2f(-5, -y)
            glVertex2f(5, -y)
            glEnd()

    def draw_origin(self):
        """Dibuja un punto o círculo pequeño en el origen (0,0)"""
        glColor3f(1.0, 0.0, 0.0)  # Color rojo para el origen
        glPointSize(8)
        glBegin(GL_POINTS)
        glVertex2f(0, 0)
        glEnd()

    def draw_circle(self, cx, cy, radius):
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(cx, cy)  # Centro del círculo
        for i in range(361):
            angle = i * math.pi / 180
            glVertex2f(cx + radius * math.cos(angle), cy + radius * math.sin(angle))
        glEnd()

    def draw_triangle(self, cx, cy, base, height):
        glBegin(GL_TRIANGLES)

        # Vértice inferior izquierdo
        glVertex2f(cx - base / 2, cy - height / 2)

        # Vértice inferior derecho
        glVertex2f(cx + base / 2, cy - height / 2)

        # Vértice superior (apex)
        glVertex2f(cx, cy + height / 2)
        glEnd()

    def draw_rectangle(self, x, y, width, height):
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

    def calculate_area_perimeter(self):
        """Calcula el área y perímetro de la figura seleccionada"""
        if self.figure == "Círculo":
            self.area = math.pi * (self.width ** 2)
            self.perimeter = 2 * math.pi * self.width
        elif self.figure == "Triángulo":
            self.area = 0.5 * self.width * self.height
            self.perimeter = self.width + 2 * math.sqrt((self.width / 2) ** 2 + self.height ** 2)
        elif self.figure == "Cuadrado":
            self.area = self.width ** 2
            self.perimeter = 4 * self.width
        elif self.figure == "Rectángulo":
            self.area = self.width * self.height
            self.perimeter = 2 * (self.width + self.height)


class Sidebar(QWidget):
    def __init__(self, opengl_widget):
        super(Sidebar, self).__init__()
        self.selected_color = QColor(0, 0, 0)
        self.opengl_widget = opengl_widget

        # Establecer el ancho máximo del sidebar
        self.setMaximumWidth(300)

        # Layout principal
        layout = QVBoxLayout()

        layout.setSpacing(15)  # Espaciado entre widgets (5 píxeles)

        # Selector de figura
        self.figure_selector = QComboBox(self)
        self.figure_selector.addItems(["Círculo", "Triángulo", "Cuadrado", "Rectángulo"])
        self.figure_selector.currentIndexChanged.connect(self.figure_selected)
        self.figure_selector_label = QLabel("Seleccionar Figura:")
        self.figure_selector_label.setMaximumHeight(50)
        layout.addWidget(self.figure_selector_label)
        layout.addWidget(self.figure_selector)

        # Selector de dimensiones (usaremos SpinBoxes)
        self.width_selector = QSpinBox(self)
        self.width_selector.setRange(1, 500)
        self.width_selector_label = QLabel("Radio:")
        self.width_selector_label.setMaximumHeight(50)
        layout.addWidget(self.width_selector_label)
        layout.addWidget(self.width_selector)

        self.height_selector = QSpinBox(self)
        self.height_selector.setRange(1, 500)
        self.height_selector_label = QLabel("Altura:")
        self.height_selector_label.setMaximumHeight(50)
        self.height_selector.hide()  # Ocultar el selector de altura por defecto
        self.height_selector_label.hide()
        layout.addWidget(self.height_selector_label)
        layout.addWidget(self.height_selector)

        row = QHBoxLayout()
        # Selector de color
        self.color_button = QPushButton("Seleccionar Color", self)
        self.color_button.setObjectName("color_button")  # Asignar ID para estilo personalizado
        self.color_button_label = QLabel("")
        self.color_button_label.setStyleSheet("background-color: #000")
        self.color_button_label.setMaximumHeight(50)
        self.color_button.clicked.connect(self.select_color)
        row.addWidget(self.color_button)
        row.addWidget(self.color_button_label)
        layout.addLayout(row)

        # Botón para graficar
        self.plot_button = QPushButton("Graficar", self)
        self.plot_button.clicked.connect(self.plot_figure)
        layout.addWidget(self.plot_button)

        layout.addStretch()
        self.setLayout(layout)

    def select_color(self):
        # Abrir el diálogo de selección de color
        self.selected_color = QColorDialog.getColor() or self.selected_color
        self.color_button_label.setStyleSheet(f"background-color: {self.selected_color.name()}")

    def figure_selected(self):
        # mostrar u ocultar el selector de altura según la figura seleccionada, también cambiar el texto del label
        figure = self.figure_selector.currentText()
        if figure == "Círculo":
            self.height_selector.hide()
            self.height_selector_label.hide()
            self.width_selector_label.setText("Radio:")
        elif figure == "Cuadrado":
            self.height_selector.hide()
            self.height_selector_label.hide()
            self.width_selector_label.setText("Lado:")
        else:
            self.height_selector.show()
            self.height_selector_label.show()
            self.width_selector_label.setText("Base:")
            self.height_selector_label.setText("Altura:")

    def plot_figure(self):
        # Obtener la figura seleccionada
        figure = self.figure_selector.currentText()
        width = self.width_selector.value()
        height = self.height_selector.value()

        # Convertir el color seleccionado a valores RGB normalizados
        color = (
            self.selected_color.red() / 255.0, self.selected_color.green() / 255.0, self.selected_color.blue() / 255.0)

        # Enviar los parámetros seleccionados al OpenGLWidget
        self.opengl_widget.set_figure(figure, width, height, color)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Hoja de estilos CSS para el sidebar en PyQt5
        sidebar_styles = """
                    QWidget {
                        background-color: #333;
                        color: #EEE;
                        font-size: 10pt;
                        font-family: Arial, sans-serif;
                    }
                    QLabel {
                        color: #CCC;
                    }
                    QLineEdit, QComboBox {
                        background-color: #555;
                        color: #EEE;
                        border: 1px solid #777;
                        border-radius: 5px;
                        padding: 5px;
                    }
                    QPushButton {
                        background-color: #666;
                        color: #EEE;
                        border: 2px solid #555;
                        border-radius: 5px;
                        padding: 5px;
                        min-height: 15px;
                    }
                    QPushButton:hover {
                        background-color: #777;
                    }
                    QPushButton:pressed {
                        background-color: #888;
                    }
                    QPushButton:disabled {
                        background-color: #444;
                        color: #888;
                    }
                """

        # Aplicar la hoja de estilos al sidebar
        self.setStyleSheet(sidebar_styles)

        self.setWindowTitle("Graficador de Figuras Geométricas")
        self.setGeometry(100, 100, 800, 600)

        # Crear los widgets
        self.opengl_widget = OpenGLWidget()
        self.sidebar = Sidebar(self.opengl_widget)

        # Crear el layout principal
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.opengl_widget)

        # Crear el widget contenedor
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
