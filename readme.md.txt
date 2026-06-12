# 🎰 Sistema de Cajero Automático - Casino UTN

Este proyecto consiste en el desarrollo de un **Asistente Virtual Automatizado (Chatbot)** integrado con la plataforma Telegram. El sistema simula las operaciones esenciales de un cajero automático de casino, administrando usuarios, controlando saldos en tiempo real y aplicando reglas de negocio mediante una arquitectura conversacional de máquina de estados.

Desarrollado para la cátedra de **Organización Empresarial** en la **Universidad Tecnológica Nacional (UTN)**.

---

## 🚀 Características Principales

- **Gestión de Estados:** Implementación de flujos conversacionales mediante `ConversationHandler` para guiar al usuario de forma intuitiva.
- **Validación de Identidad:** Sistema automatizado de control de credenciales de jugadores con manejo de errores de entrada (Camino Infeliz).
- **Reglas de Negocio (Gateways):** Control estricto de transacciones mediante compuertas lógicas (`if/else`) para evitar extracciones con fondos insuficientes.
- **Persistencia de Datos Simulada:** Diccionario de datos indexado en memoria para mantener consistencia de saldos durante la sesión.
- **Auditoría Técnica:** Módulo de `logging` integrado para el registro continuo de eventos y fiscalización en la consola del servidor.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.10+
- **Librería Principal:** `python-telegram-bot` (v20.x o superior)
- **Entorno de Desarrollo:** Visual Studio Code & Git
- **Modelado de Procesos:** BPMN 2.0 (Lucidchart)

---

## 📦 Estructura del Proyecto

```text
├── bot.py           # Código fuente principal del Chatbot y lógica de negocio
├── README.md        # Documentación técnica del repositorio (este archivo)
└── .gitignore       # Exclusión de credenciales (API Tokens) y entorno virtual (/venv/)