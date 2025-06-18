import sys
import socket
import webbrowser
import qrcode
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No necesita conexión real, solo para detectar la interfaz de red
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "IP NO DISPONIBLE"
    finally:
        s.close()
    return ip


def generar_qr(data, filename="qr.png"):
    img = qrcode.make(data)
    img.save(filename)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(800, 500)
        self.setWindowTitle("MesApp")
        self.setStyleSheet("background-color: #1F484E;")

        # Layout principal horizontal sin márgenes ni separación
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        self.main_layout.setSpacing(0)  # Sin separación entre contenedores
        self.setLayout(self.main_layout)

        # --- CONTENEDOR IZQUIERDO COMO WIDGET ---
        self.left_widget = QWidget()
        self.left_widget.setStyleSheet(
            """
            background-color: #D9D9D9;
            border-top-right-radius: 60px;
            border-bottom-right-radius: 60px;
        """
        )
        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignCenter)  # Centrado total
        self.left_widget.setLayout(self.left_layout)

        self.left_layout.addStretch()  # Espacio arriba

        # Agregar logo centrado
        logo_label = QLabel()
        pixmap = QPixmap("logo.png")
        logo_label.setPixmap(pixmap)
        scaled_pixmap = pixmap.scaled(
            200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        self.left_layout.addWidget(logo_label)

        # Label de estado debajo del logo
        status_label = QLabel("El sistema se está ejecutando")
        status_label.setStyleSheet(
            """
            color: #0A150E;
            font-family: Inter;
            font-size: 20px;
            font-weight: 500;
        """
        )
        status_label.setAlignment(Qt.AlignCenter)
        self.left_layout.addWidget(status_label)

        # Obtener IP del dispositivo
        local_ip = get_local_ip()
        url = f"https://{local_ip}:3000"
        generar_qr(url, "qr.png")
        webbrowser.open(url)

        # Contenedor tipo label con estilo y enlace HTML
        url_label = QLabel(f'<a href="{url}">{url}</a>')
        url_label.setOpenExternalLinks(True)
        url_label.setStyleSheet(
            """
            background-color: white;
            border-radius: 15px;
            padding: 10px 20px;
            font-family: Inter;
            font-size: 14px;
            font-weight: bold;
            color: #FFFFFF;
        """
        )
        url_label.setAlignment(Qt.AlignCenter)
        self.left_layout.addWidget(url_label)

        # Contenedor visual para el QR con fondo blanco y esquinas redondeadas
        qr_container = QWidget()
        qr_container.setFixedSize(210, 210)
        qr_container.setStyleSheet(
            """
            background-color: white;
            border-radius: 40px;
        """
        )
        qr_layout = QVBoxLayout()
        qr_layout.setContentsMargins(20, 20, 20, 20)  # Espaciado interno
        qr_layout.setAlignment(Qt.AlignCenter)
        qr_container.setLayout(qr_layout)

        # QR code (solo la imagen generada)
        qr_label = QLabel()
        qr_label.setPixmap(
            QPixmap("qr.png").scaled(
            200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        qr_label.setAlignment(Qt.AlignCenter)
        qr_layout.addWidget(qr_label)

        # Agregar el contenedor debajo del enlace y centrarlo
        self.left_layout.addWidget(qr_container, alignment=Qt.AlignCenter)

        self.left_layout.addStretch()  # Espacio abajo

        # --- CONTENEDOR DERECHO COMO LAYOUT ---
        self.right_layout = QVBoxLayout()

        # Agregar los widgets al layout principal
        self.main_layout.addWidget(self.left_widget, 1)
        self.main_layout.addLayout(self.right_layout, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
