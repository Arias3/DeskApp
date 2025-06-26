import sys
import socket
import webbrowser
import qrcode
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSizeF, QRectF
from PyQt5.QtGui import QPixmap
from PyQt5.QtPrintSupport import QPrinterInfo
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QPushButton
from jinja2 import Template
import datetime
import json
import threading
import websockets
import asyncio
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
import winsound
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables del archivo .env

WS_HOST = os.getenv("WS_HOST", "localhost")
WS_PORT = int(os.getenv("WS_PORT", 3000))

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

    imprimir_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("./assets/logo.ico"))
        self.iniciar_servidor_websocket(WS_HOST, WS_PORT)
        self.imprimir_signal.connect(self.imprimir_comanda)

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
        pixmap = QPixmap("./assets/logo.png")
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
        url = f"http://{local_ip}:5173"
        generar_qr(url, "qr.png")
        # webbrowser.open(url)

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
        self.right_layout.setAlignment(Qt.AlignCenter)  # Centra todo el contenido

        # Agregar label de selección de impresora
        printer_label = QLabel("Seleccione una impresora:")
        printer_label.setStyleSheet(
            """
            color: #FFFFFF;
            font-family: Inter;
            font-size: 18px;
            font-weight: bold;
        """
        )
        printer_label.setAlignment(Qt.AlignCenter)  # Centra el texto en el label
        self.right_layout.addWidget(printer_label)

        self.right_layout.addSpacing(24)

        # Contenedor visual para el combo
        combo_container = QWidget()
        combo_container.setFixedSize(340, 60)
        combo_container.setStyleSheet(
            """
            background-color: #D9D9D9;
            border-radius: 16px;
        """
        )
        combo_layout = QVBoxLayout()
        combo_layout.setContentsMargins(12, 6, 12, 6)
        combo_layout.setAlignment(Qt.AlignCenter)
        combo_container.setLayout(combo_layout)

        # Menú desplegable personalizado
        self.printer_combo = QComboBox()
        self.printer_combo.setFixedHeight(46)
        self.printer_combo.setStyleSheet(
            """
            QComboBox {
                background-color: #D9D9D9;
                border: none;
                border-radius: 18px;
                padding: 8px 48px 8px 12px;
                font-family: Inter, Arial, sans-serif;
                font-size: 22px;
                color: #1F484E;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 44px;
                border: none;
            }

            QComboBox::down-arrow {
                image: url(assets/arrow-down.svg); /* Asegúrate de que esta ruta sea válida */
                width: 36px;
                height: 36px;
                margin-right: 10px;
            }

            QComboBox QAbstractItemView {
                background-color: #F5F5F5;
                border-radius: 10px;
                font-family: Inter, Arial, sans-serif;
                font-size: 16px;
                color: #1F484E;
                selection-background-color: #bfc0c0;
                outline: none;
                padding: 6px;
            }
        """
        )

        self.printer_combo.addItem("")  # Inicialmente en blanco

        # Obtener impresoras disponibles y agregarlas al combo
        printers = QPrinterInfo.availablePrinters()
        for printer in printers:
            self.printer_combo.addItem(printer.printerName())

        combo_layout.addWidget(self.printer_combo)
        self.right_layout.addWidget(combo_container, alignment=Qt.AlignCenter)

        self.right_layout.addSpacing(24)

        # Datos de prueba con fecha actual
        ahora = datetime.datetime.now()
        datos_prueba = {
            "numero": "0001",
            "fecha": ahora.strftime("%Y-%m-%d"),
            "hora": ahora.strftime("%H:%M"),
            "Mesa": "Mesa 1",
            "items": [
                {
                    "nombre": "Helado Mixto",
                    "sabores": "Fresa - Limón - Vainilla",
                    "notas": "Pedir con cono doble, extra topping de chispas",
                },
            ],
        }

        # Botón de imprimir
        print_button = QPushButton("Imprimir Prueba")
        print_button.setFixedSize(200, 50)
        print_button.setStyleSheet(
            """
            QPushButton {
                background-color: #D9D9D9;
                color: #0A150E;
                font-family: Inter;
                font-size: 18px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: white;
            }
        """
        )
        print_button.clicked.connect(lambda: self.imprimir_comanda(datos_prueba))
        self.right_layout.addWidget(print_button, alignment=Qt.AlignCenter)

        # Agregar los widgets al layout principal
        self.main_layout.addWidget(self.left_widget, 1)
        self.main_layout.addLayout(self.right_layout, 1)

    def iniciar_servidor_websocket(self, host="localhost", puerto=3000):
        async def manejador(websocket):
            print(f"🟢 Cliente conectado desde {websocket.remote_address}")
            try:
                async for mensaje in websocket:
                    print(f"📨 Mensaje recibido: {mensaje}")
                    try:
                        datos = json.loads(mensaje)
                        if all(k in datos for k in ["numero", "fecha", "hora", "items"]):
                            self.imprimir_signal.emit(datos)
                        else:
                            print("❌ Datos incompletos, se ignora el mensaje.")
                    except Exception as e:
                        print(f"❌ Error procesando mensaje: {e}")
            except websockets.ConnectionClosed:
                print("🔌 Cliente desconectado.")

        async def iniciar():
            print(f"🌐 Iniciando servidor WebSocket en ws://{host}:{puerto} ...")
            async with websockets.serve(manejador, host, puerto, process_request=None):  
                await asyncio.Future()  # mantener corriendo

        def run_loop():
            asyncio.set_event_loop(asyncio.new_event_loop())
            asyncio.get_event_loop().run_until_complete(iniciar())

        threading.Thread(target=run_loop, daemon=True).start()
    @pyqtSlot(dict)
    def imprimir_comanda(self, datos):

        selected_printer_name = self.printer_combo.currentText()
        if not selected_printer_name:
            print("No se ha seleccionado una impresora.")
            return

        # ========== PASO 1: CALCULAR ALTO REAL DEL CONTENIDO ==========
        from PyQt5.QtGui import QPixmap, QPainter, QFont
        from PyQt5.QtCore import Qt

        ancho_virtual = int(58 * 3.78)  # fuerza a int directamente

        y = 10  # Espacio superior inicial
        logo_path = "./assets/capri.png"
        logo_height = 0

        try:
            logo = QPixmap(logo_path).scaledToWidth(60, Qt.SmoothTransformation)
            logo_height = logo.height()
        except:
            logo_height = 0

        y += logo_height + 20  # espacio después del logo

        # Pintor virtual para medir texto
        pixmap_virtual = QPixmap(ancho_virtual, 2000)
        pixmap_virtual.fill(Qt.white)
        medidor = QPainter(pixmap_virtual)

        medidor.setFont(QFont("Courier New", 11, QFont.Bold))
        y += (
            medidor.boundingRect(
                0, 0, ancho_virtual, 9999, Qt.TextWordWrap, f"ORDEN #{datos['numero']}"
            ).height()
            + 4
        )

        medidor.setFont(QFont("Courier New", 8))
        y += (
            medidor.boundingRect(
                0,
                0,
                ancho_virtual,
                9999,
                Qt.TextWordWrap,
                f"Fecha: {datos['fecha']}   Hora: {datos['hora']}",
            ).height()
            + 8
        )

        medidor.setFont(QFont("Courier New", 11, QFont.Bold))
        y += (
            medidor.boundingRect(
                0, 0, ancho_virtual, 9999, Qt.TextWordWrap, f"Mesa: {datos['Mesa']}"
            ).height()
            + 4
        )

        y += 10  # Línea divisoria

        for item in datos["items"]:
            medidor.setFont(QFont("Courier New", 9, QFont.Bold))
            y += (
                medidor.boundingRect(
                    0, 0, ancho_virtual, 9999, Qt.TextWordWrap, item["nombre"]
                ).height()
                + 4
            )

            medidor.setFont(QFont("Courier New", 8))
            sabor_texto = f"Sabor: {item['sabores']}"
            y += (
                medidor.boundingRect(
                    0, 0, ancho_virtual - 20, 9999, Qt.TextWordWrap, sabor_texto
                ).height()
                + 5
            )

            notas_texto = f"Notas: {item['notas']}"
            y += (
                medidor.boundingRect(
                    0, 0, ancho_virtual - 20, 9999, Qt.TextWordWrap, notas_texto
                ).height()
                + 5
            )

            y += 10  # línea divisoria

        y += 30  # espacio final

        medidor.end()

        # === Conversión precisa de píxeles a milímetros ===
        dpi = pixmap_virtual.logicalDpiY()
        alto_mm = max(60, int((y / dpi) * 22) + 1)

        # ========== PASO 2: CONFIGURAR IMPRESORA ==========
        printer = QPrinter()
        printer.setPrinterName(selected_printer_name)
        printer.setOutputFormat(QPrinter.NativeFormat)
        printer.setPageSize(QPrinter.Custom)
        printer.setPaperSize(QSizeF(58, alto_mm), QPrinter.Millimeter)
        printer.setFullPage(True)
        printer.setPageMargins(3, 3, 3, 3, QPrinter.Millimeter)

        # ========== PASO 3: IMPRIMIR ==========
        painter = QPainter()
        if not painter.begin(printer):
            print("No se pudo iniciar la impresión.")
            return

        ancho_papel = printer.pageRect().width()
        y = 30

        try:
            logo = QPixmap(logo_path).scaledToWidth(100, Qt.SmoothTransformation)
            x_logo = (ancho_papel - logo.width()) // 2
            painter.drawPixmap(x_logo, int(y), logo)
            y += logo.height() + 20
        except:
            print("Logo no encontrado, se omite.")
            y += 20

        # ORDEN
        painter.setFont(QFont("Courier New", 15, QFont.Bold))
        orden_text = f"ORDEN #{datos['numero']}"
        orden_rect = QRectF(0, y, ancho_papel, 9999)
        painter.drawText(orden_rect, Qt.AlignHCenter | Qt.TextWordWrap, orden_text)
        orden_height = painter.boundingRect(
            orden_rect, Qt.AlignHCenter | Qt.TextWordWrap, orden_text
        ).height()
        y += orden_height + 4

        # FECHA HORA
        painter.setFont(QFont("Courier New", 8))
        painter.drawText(0, int(y), f"Fecha: {datos['fecha']}   Hora: {datos['hora']}")
        y += 15

        painter.setFont(QFont("Courier New", 11, QFont.Bold))
        mesa_text = f"Mesa: {datos['Mesa']}"
        mesa_rect = QRectF(0, y, ancho_papel, 9999)
        painter.drawText(mesa_rect, Qt.AlignHCenter | Qt.TextWordWrap, mesa_text)
        mesa_height = painter.boundingRect(
            mesa_rect, Qt.AlignHCenter | Qt.TextWordWrap, mesa_text
        ).height()
        y += mesa_height + 4

        # LINEA
        painter.drawLine(0, int(y), int(ancho_papel), int(y))
        y += 12

        # ITEMS
        for item in datos["items"]:
            painter.setFont(QFont("Courier New", 9, QFont.Bold))
            painter.drawText(0, int(y), item["nombre"])
            y += 14

            sabor_texto = f"Sabor: {item['sabores']}"
            sabor_rect = QRectF(10, y, ancho_papel - 20, 9999)
            sabor_flags = Qt.TextWordWrap
            painter.setFont(QFont("Courier New", 8))
            painter.drawText(sabor_rect, sabor_flags, sabor_texto)
            sabor_height = painter.boundingRect(
                sabor_rect, sabor_flags, sabor_texto
            ).height()
            y += sabor_height + 5

            notas_texto = f"Notas: {item['notas']}"
            notas_rect = QRectF(10, y, ancho_papel - 20, 9999)
            notas_flags = Qt.TextWordWrap
            painter.drawText(notas_rect, notas_flags, notas_texto)
            notas_height = painter.boundingRect(
                notas_rect, notas_flags, notas_texto
            ).height()
            y += notas_height + 5

            painter.drawLine(0, int(y), int(ancho_papel), int(y))
            y += 12

        painter.end()
        winsound.PlaySound("./assets/notification.wav", winsound.SND_FILENAME)

        print(f"✅ Factura generada con alto dinámico: {alto_mm} mm")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
