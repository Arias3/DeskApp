# 🖥️ Sistema de Recepción de Pedidos - Cliente de Impresión (PyQt5)

Este proyecto es una aplicación de escritorio desarrollada en **Python** utilizando la librería **PyQt5** para la interfaz gráfica. Su función principal es actuar como cliente de impresión en un sistema de pedidos para restaurantes, comunicándose con una aplicación web (que posee su propio repositorio).

## 🚀 Funcionalidades

- 🖨️ **Impresión automática de pedidos** recibidos desde la aplicación web mediante **WebSockets**.
- 🔌 **Ejecución de servidores locales** necesarios para la comunicación entre sistemas.
- 📎 **Selección de impresora** de 80mm desde la interfaz.
- 🔄 **Reinicio manual de los servidores** con un solo clic.
- 📱 **Generación automática de un código QR** para facilitar el acceso a la aplicación web desde otros dispositivos.

## 🌐 Aplicación Web

> Este cliente está diseñado para trabajar en conjunto con una aplicación web para la toma de pedidos, la cual se encuentra en un **repositorio independiente**.

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **PyQt5**
- **WebSockets**
- **QZ Tray / impresión directa**
- **Servidor local (Flask, FastAPI o similar según implementación)**

## 📸 Interfaz y Acceso Rápido
![INTERFAZ](./app.png)
