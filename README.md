# 🛒 Gestor de Supermercado (Python POS)

Un sistema de **Punto de Venta (POS)** de escritorio desarrollado en **Python** utilizando **Tkinter** para la interfaz gráfica y **SQL Server** para la gestión de datos. El sistema permite realizar ventas, gestionar inventario en tiempo real y manejar múltiples usuarios mediante autenticación directa con la base de datos.

## Características

* **Autenticación Segura:** Inicio de sesión validado directamente contra los usuarios de SQL Server.
* **Dashboard de Ventas:**
    * Búsqueda de productos por clave.
    * Visualización de carrito de compras con `Treeview`.
    * Cálculo automático de subtotales y totales.
* **Integridad de Datos (ACID):** Manejo robusto de transacciones. Si una venta falla a la mitad, se revierten todos los cambios (Rollback) para evitar inconsistencias en el inventario.
* **Gestión de Concurrencia:** Bloqueo de filas (`UPDLOCK`) al obtener folios para evitar duplicidad de tickets en cajas simultáneas.
* **Control de Stock:** Validación automática de existencias antes de agregar productos al carrito.

## Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Interfaz Gráfica:** Tkinter (Librería estándar)
* **Base de Datos:** Microsoft SQL Server
* **Conector:** `pyodbc`
* **Driver:** ODBC Driver 17 for SQL Server

## Configuración e Instalación

### 1. Requisitos Previos
Necesitas tener instalado Python y el driver ODBC de Microsoft. Además, instala la librería de conexión:

```bash
pip install pyodbc
```
## 2. Configuración de la Base de Datos
El sistema requiere una base de datos llamada PuntoDeVenta en SQL Server. Asegúrate de tener las siguientes tablas creadas para que el código funcione:

```SQL
-- Estructura inferida
CREATE DATABASE PuntoDeVenta;
GO
USE PuntoDeVenta;

CREATE TABLE Producto (
    claveProducto INT PRIMARY KEY,
    descProd VARCHAR(100),
    precio DECIMAL(10,2),
    stock INT
);

CREATE TABLE Sucursal (
    idSucursal INT PRIMARY KEY,
    folioVentaActual INT
);

CREATE TABLE Venta (
    idVenta INT PRIMARY KEY,
    idSucursal INT,
    total DECIMAL(10,2)
);

CREATE TABLE DetalleVenta (
    idVenta INT,
    claveProducto INT,
    cantidad INT,
    precio DECIMAL(10,2),
    FOREIGN KEY (idVenta) REFERENCES Venta(idVenta)
);

-- Inicialización requerida
INSERT INTO Sucursal VALUES (1, 0); -- Inicia el contador de folios
```
## 3. Conexión
**Advertencia de Seguridad:** Actualmente las credenciales de administrador (sa) están visibles en el código fuente (conexion_db.py). Para un entorno de producción, se recomienda usar variables de entorno.

Verifica que los datos en conexion_db.py coincidan con tu servidor:
```Python
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=TU_SERVIDOR_IP;"  -- Ej: 129.158.255.133
    "PORT=1433;"
    "DATABASE=PuntoDeVenta;"
    "UID=sa;"
    "PWD=TU_CONTRASEÑA;"
)
```
## Ejecución
Para iniciar la aplicación, ejecuta el archivo de login:
```bash
python login.py
```
1. Ingresa tu usuario y contraseña de SQL Server (o usuarios creados en la BD).
2. Al acceder, se abrirá el **Dashboard**.
3. Ingresa la clave del producto y la cantidad, luego presiona Enter o el botón "Agregar".
4. Para finalizar, presiona "Registrar Venta".

## Estructura del Proyecto

  login.py          # Ventana de inicio de sesión (Entry Point)
  dashboard.py      # Lógica principal del punto de venta y UI
  conexion_db.py    # Módulo de conexión y strings de conexión ODBC
  
## 👤 Autor
Desarrollado como proyecto académico de software para gestión de ventas.
