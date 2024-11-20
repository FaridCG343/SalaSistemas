`README.txt`:

```
# Proyecto de Python

Este proyecto requiere la instalación de ciertas librerías especificadas en el archivo `requirements.txt`. Sigue las instrucciones a continuación para configurar el entorno y ejecutar el script.

---

## Requisitos previos

1. **Python instalado**: Asegúrate de tener Python 3.x instalado en tu sistema. Puedes descargarlo desde https://www.python.org/.

2. **pip instalado**: pip viene generalmente con Python. Verifica la instalación ejecutando el siguiente comando:
   ```
   pip --version
   ```

---

## Instrucciones de instalación

1. Clona este repositorio o descarga los archivos en tu sistema.

2. Abre una terminal en la carpeta donde se encuentra el archivo `requirements.txt`.

3. Si deseas, crea un entorno virtual para evitar conflictos de dependencias:
   ```
   python -m venv venv
   source venv/bin/activate      # En Linux/Mac
   venv\Scripts\activate         # En Windows
   ```

4. Instala las dependencias ejecutando:
   ```
   pip install -r requirements.txt
   ```

---

## Ejecución del script

1. Una vez que las dependencias estén instaladas, ejecuta el script principal con el siguiente comando:
   ```
   python SalaSistemas.py
   ```

---

## Notas adicionales

- Si encuentras algún problema, asegúrate de estar usando la versión correcta de Python y de que las dependencias estén instaladas correctamente.
- Si el entorno virtual está activado, recuerda desactivarlo cuando termines con:
  ```
  deactivate
  ```
```