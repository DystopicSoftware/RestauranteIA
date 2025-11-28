# 🍔 RestauranteIA - Sistema de Gestión Inteligente

![Python 3.10.19](https://img.shields.io/badge/Python-3.10.19-blue.svg)
![Status](https://img.shields.io/badge/Status-Migrado%20de%20Colab-green.svg)

Sistema de gestión de inventarios y ventas para un restaurante, potenciado con Inteligencia Artificial (LangChain + Ollama Llama3) y una arquitectura modular en Python.

Este proyecto fue originalmente prototipado en **Google Colab** y refactorizado para ejecutarse en un entorno local robusto.

## ⚠️ Importante: Compatibilidad de Versiones

Debido a la migración desde un entorno de Colab y a la rápida evolución de las librerías de IA (LangChain, Ollama), **es estrictamente necesario utilizar Python 3.10.19**.

Versiones más recientes (3.11/3.12) o más antiguas pueden generar conflictos con dependencias específicas o métodos deprecados utilizados en el flujo lógico del agente.

Se recomienda encarecidamente el uso de **Conda** para gestionar este entorno aislado.

## 🚀 Características

- **Asistente Virtual Híbrido:** Dos modos de operación (Administrador y Cliente) usando `ChatOllama`.
- **Gestión de Inventario:** Control de stock, ingredientes y recetas dinámicas.
- **Análisis de Datos:** KPIs, reportes de ventas y generación de gráficos automáticos con `Matplotlib`.
- **Persistencia:** Base de datos SQLite local (`restaurante.db`) con actualización automática.
- **Arquitectura Modular:** Código organizado en capas (`Data`, `Utils`, `Funciones`, `Tools`, `Agents`) para fácil mantenimiento.

## 🛠️ Instalación y Configuración

Sigue estos pasos para replicar el entorno de desarrollo exacto:

### 1. Clonar el repositorio

git clone https://github.com/TU_USUARIO/RestauranteIA.git
cd RestauranteIA

### 2. Crear Entorno Virtual con Conda (Recomendado)
Para asegurar la compatibilidad mencionada (Python 3.10.19):

# Crear el entorno con la versión específica
conda create -n restaurante python=3.10.19

# Activar el entorno
conda activate restaurante

### 3. Instalar Dependencias
Una vez activo el entorno, instala las librerías necesarias:

pip install -r requirements.txt

### 4. Configurar Ollama
Este proyecto utiliza Ollama ejecutándose localmente.
Descarga e instala Ollama.
Descarga el modelo llama3 (o el que tengas configurado en config/settings.py):

ollama pull llama3

### 5. Ejecución
python app.py

# 🏗️ Estructura del Proyecto
/agents: Configuración de los agentes de LangChain (Admin/Cliente).


/config: Configuraciones generales y conexión con el LLM.


/data: Datos iniciales (seeding) de productos e inventario.


/database: Gestión de conexión y persistencia con SQLite.


/funciones: Lógica de negocio pura (Cálculo de KPIs, operaciones de inventario).


/tools: Herramientas (Tools) que conectan las funciones con la IA.


/utils: Utilidades de procesamiento de texto y fuzzy matching.


📄 Notas de Migración


Si vienes del notebook original de Colab, notarás que las celdas monolíticas se han separado en módulos .py específicos. Esto facilita la depuración y permite que la aplicación crezca sin volverse inmanejable.

Hecho con 🍔 y Python.
