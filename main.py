import sys
import os
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QLabel, QScrollArea, QWidget, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import Qt, QUrl, QObject, pyqtSlot
from PyQt5.QtGui import QPixmap, QImage

# ====== MAPA: clave -> número de página en el PDF ======
MAPA = {

     #Artículos ya existentes
    "art200": 42,
    "art220": 63,
    "art220-12": 64,
    "art220-14": 65,
    "art220-52": 68,
    "art220-18": 67,
    "art430": 402,
    "art440": 443,
    "art220-50": 68,
    "art220-51": 68,
    "art220-54": 69,
    "art220-55": 69,
    "art620": 711,
    "art695": 824,
    "art670": 763,
    "art445": 452,
    "art450": 454,
    "art460": 466,
    "art470": 469,
    "art680": 768,
    "art690": 792,
    "art692": 812,
    "art694": 815,
    "art220-42": 67,
    "art220-44": 68,
    "art220-54": 69,
    "art220-55": 69,
    "art220-56": 70,
    "art620-14": 715,
    "art630": 736,
    "art210": 45,
    "art220-10": 64,
    "art220-87": 75,
    "art215": 60,
    "Art110.14(C)": 30,
    "art240-6": 103,
    "art210-19": 51,
    "art215-2": 61,
    "art520-27": 612,
    "art551-73": 667,
    "art695-7": 831,
    "art647-4": 752,
    "art630-11": 738,
    "art630-31": 739,
    "art555-12": 685,
    "art430-31": 416,

    #Artículos faltantes necesitas proporcionar los números de página correctos
    "art450-11": 460,
    "art450-2": 455,
    "art450-9": 456,
    "art450-13": 457,
    "art450-21": 458,
    "art450-14": 457,
    "art310": 180,
    "art450-3": 455,
    "art240": 99,
    
    

    #Tablas
    "tab220-42": 67,
    "tab220-54": 69,
    "tab220-55": 69,
    "tab310-15b16": 189,
    "tab310-15b2b": 185,
    "tabla220": 64,
    "tabla240": 100,
    "tabla310-15": 185,
    "tab430-147": 435,
    "tab430-148": 431,
    "tab310-15b3a": 186,
    "tab9": 1010,
    "tab250-1133": 150,

    #Artículos adicionales del sistema de tierras
    "art250": 250,
    "art250-50": 255,
    "art250-52": 256,
    "art800-53": 850,
    "tabla250-66": 265,
    "tabla250-102": 268,
    "tabla250-112": 150,
    
    #Artículos de canalizaciones
    "art358": 277,
    "art342": 255,
    "art344": 257,
    "art352": 264,
    "art392": 309,
    "art366": 285,
    "cap9tablas": 1001,
    
    #Artículos de áreas clasificadas y especiales
    "art500": 500,
    "art500-5": 502,
    "art500-7": 503,
    "art500-8": 504,
    "art501-10": 510,
    "art501-15": 515,
    "art502-10": 520,
    "art503-10": 530,
    "art516": 540,
    
    #Artículos de tableros y CCM
    "art110-26": 110,
    "art408": 408,
    "art430-102": 420,
    "art430-52": 415,
    "art430-32": 410,
    "art430-24": 414,
    "art430-25": 414,
    "art430-26": 414,
    "art430-47": 43,
    "art440-6": 445,
    #Artículos de instalaciones especiales
    "art680-21": 770,
    "art680-22": 771,
    "art680-25": 772,
    "art680-51": 775,
    "art300-5": 305,
    
    #Artículos de sistemas de emergencia
    "art700-5": 830,
    "art700-10b": 832,
    "art700-12": 833,
    "art702-4": 840,
    "art702-5": 841,
    
    #Artículos de sistemas fotovoltaicos
    "art690-7a": 795,
    "art690-8": 796,
    "art690-9": 797,
    "art690-14": 800,
    "art690-15": 801,
    "art690-31": 805,
    "art690-56": 808,
    "art705": 850,
    
    #Referencias generales
    "nom001": 1,
    
}

# ====== PDF Viewer ======
class PDFViewer(QScrollArea):
    def __init__(self, pdf_path):
        super().__init__()
        self.doc = fitz.open(pdf_path)
        self.pagina_actual = 0
        self.zoom = 1.5

        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.setWidget(container)
        self.setWidgetResizable(True)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Botones flotantes y QLineEdit
        self.btn_container = QWidget(self)
        from PyQt5.QtWidgets import QHBoxLayout
        btn_layout = QHBoxLayout(self.btn_container)
        self.btn_container.setLayout(btn_layout)

        self.btn_prev = QPushButton("Anterior")
        self.btn_next = QPushButton("Siguiente")
        self.btn_zoom_in = QPushButton("Zoom +")
        self.btn_zoom_out = QPushButton("Zoom -")
        self.page_input = QLineEdit()
        self.page_input.setFixedWidth(50)
        self.page_input.setAlignment(Qt.AlignCenter)
        self.page_input.setPlaceholderText("Página")
        self.page_input.returnPressed.connect(self.ir_a_pagina)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_prev)
        btn_layout.addWidget(self.btn_next)
        btn_layout.addWidget(self.btn_zoom_in)
        btn_layout.addWidget(self.btn_zoom_out)
        btn_layout.addWidget(self.page_input)
        btn_layout.addStretch()

        self.btn_prev.clicked.connect(self.anterior)
        self.btn_next.clicked.connect(self.siguiente)
        self.btn_zoom_in.clicked.connect(self.zoom_in)
        self.btn_zoom_out.clicked.connect(self.zoom_out)

        estilo_botones = """
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            padding: 5px 15px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
        QLineEdit {
            border-radius: 10px;
            border: 2px solid #4CAF50;
            padding: 5px;
            font-weight: bold;
        }
        """
        self.btn_prev.setStyleSheet(estilo_botones)
        self.btn_next.setStyleSheet(estilo_botones)
        self.btn_zoom_in.setStyleSheet(estilo_botones)
        self.btn_zoom_out.setStyleSheet(estilo_botones)
        self.page_input.setStyleSheet(estilo_botones)

        self.mostrar_pagina(0)

    def resizeEvent(self, event):
        container_width = self.width()
        container_height = self.height()
        btn_width = 500
        btn_height = 50
        x = (container_width - btn_width) // 2
        y = container_height - btn_height - 10
        self.btn_container.setGeometry(x, y, btn_width, btn_height)
        super().resizeEvent(event)

    def mostrar_pagina(self, num_pagina):
        if 0 <= num_pagina < len(self.doc):
            self.pagina_actual = num_pagina
            pagina = self.doc.load_page(num_pagina)
            matrix = fitz.Matrix(self.zoom, self.zoom)
            pix = pagina.get_pixmap(matrix=matrix)
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(img))
            self.page_input.setText(str(self.pagina_actual + 1))

    def ir_a_pagina(self):
        try:
            pagina = int(self.page_input.text()) - 1
            self.mostrar_pagina(pagina)
        except:
            pass

    def siguiente(self):
        if self.pagina_actual + 1 < len(self.doc):
            self.mostrar_pagina(self.pagina_actual + 1)

    def anterior(self):
        if self.pagina_actual - 1 >= 0:
            self.mostrar_pagina(self.pagina_actual - 1)

    def zoom_in(self):
        self.zoom += 0.25
        self.mostrar_pagina(self.pagina_actual)

    def zoom_out(self):
        if self.zoom > 0.5:
            self.zoom -= 0.25
            self.mostrar_pagina(self.pagina_actual)

    def wheelEvent(self, event):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
        else:
            super().wheelEvent(event)
            barra = self.verticalScrollBar()
            if event.angleDelta().y() < 0 and barra.value() == barra.maximum():
                self.siguiente()
            elif event.angleDelta().y() > 0 and barra.value() == barra.minimum():
                self.anterior()

# ====== Canal JS -> Python ======
class Canal(QObject):
    def __init__(self, pdf_viewer):
        super().__init__()
        self.pdf_viewer = pdf_viewer

    @pyqtSlot(str)
    def abrir_articulo(self, clave):
        if clave in MAPA:
            self.pdf_viewer.mostrar_pagina(MAPA[clave])

# ====== Ventana principal ======
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manual + NOM Viewer")
        splitter = QSplitter(Qt.Horizontal)

        # ====== Rutas para PyInstaller ======
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath("C:\\Users\\Fulano\\Documents\\Nom 2012 PROGRAMA\\Programa")

        ruta_manual = os.path.join(base_path, "manual.html")
        ruta_pdf = os.path.join(base_path, "NOM.pdf")

        # PDF Viewer
        self.pdf_viewer = PDFViewer(ruta_pdf)

        # HTML Viewer
        self.web = QWebEngineView()
        self.web.load(QUrl.fromLocalFile(ruta_manual))

        # QWebChannel
        self.canal = Canal(self.pdf_viewer)
        self.channel = QWebChannel()
        self.channel.registerObject("canal", self.canal)
        self.web.page().setWebChannel(self.channel)

        splitter.addWidget(self.web)
        splitter.addWidget(self.pdf_viewer)
        self.setCentralWidget(splitter)

# ====== Ejecución ======
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())