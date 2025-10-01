# NOM Viewer

¡Bienvenidos a **NOM Viewer**! 👋

Este es un programa hecho en **Python** que permite visualizar el manual de la NOM-SEDE-2012 en formato PDF junto con un HTML interactivo.  
Es una herramienta útil para buscar artículos, tablas y referencias rápidamente.


## Cómo usar
Descarga el pdf de la NOM-SEDE-2012( https://drive.google.com/file/d/1pD823-cEUWY1tPMqJYO96YQxuE9v3FgX/view?usp=drive_link ).
1. Clona o descarga este repositorio.
2. Instala las dependencias: `pip install -r requirements.txt`
3. Ejecuta: `python main.py`


---

## 📌 Estado del proyecto

- El PDF contiene la mayoría de los artículos, pero **faltan algunos artículos por etiquetar**.
- La funcionalidad básica está lista, pero siempre se pueden hacer mejoras en la interfaz y en la navegación.

---

## 💡 Cómo ayudar

Si quieres ayudar a mejorar el proyecto:

1. Haz un **fork** de este repositorio.  
2. Haz tus cambios en tu copia.  
3. Envía un **Pull Request (PR)** explicando tus mejoras o correcciones.  


---

## 📂 Archivos principales

- `main.py` → Código principal de la aplicación
- `NOM.pdf` → Documento de la NOM 2012
- `manual.html` → HTML interactivo con la tabla de contenidos

---

## 🚀 ¡Únete a colaborar!

Si te interesa la NOM, Python o mejorar herramientas útiles para todos, ¡estás más que invitado a contribuir!  
Cada colaboración ayuda a que el proyecto sea más completo y funcional para todos. 💪

📝 Cómo ejecutar NOM Viewer en tu computadora

Sigue estos pasos para tener tu aplicación funcionando:

1️⃣ Descargar los archivos

Descarga el proyecto desde GitHub (o donde lo tengas publicado).

Asegúrate de que los archivos principales estén en una sola carpeta, por ejemplo:

/NOM-Viewer
    ├─ main.py
    ├─ NOM.pdf
    └─ manual.html


Esto es importante: el PDF y el HTML deben estar en la misma carpeta que main.py.

2️⃣ Abrir la carpeta en Visual Studio Code

Abre Visual Studio Code.

Selecciona File → Open Folder… y abre la carpeta donde pusiste los archivos.

Ahora verás main.py y los demás archivos en el explorador de VS Code.

3️⃣ Instalar Python y bibliotecas necesarias

Asegúrate de tener Python instalado (recomendado 3.10 o superior).

Luego abre una terminal en VS Code (Terminal → New Terminal) y escribe:

pip install PyQt5 PyQtWebEngine PyMuPDF


Estas bibliotecas son necesarias para que el programa funcione:

PyQt5 → Interfaz gráfica

PyQtWebEngine → Para mostrar el HTML dentro de la app

PyMuPDF → Para abrir y mostrar el PDF

4️⃣ Ejecutar la aplicación

En la misma terminal, escribe:

python main.py


Si todo está correcto, se abrirá la ventana con el NOM Viewer, mostrando el HTML y el PDF.
