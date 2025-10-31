import pyodbc
from tkinter import messagebox
import hashlib

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=129.158.255.133;"
    "PORT=1433;"         
    "DATABASE=PuntoDeVenta;"  
    "UID=sa;"              
    "PWD=Narciso21;"              
    "TrustServerCertificate=yes;"
)

def get_connection():
    try:
        return pyodbc.connect(connection_string)
    except Exception as e:
        messagebox.showerror("Error de Conexión", f"No se pudo conectar a la BD: {e}")
        return None
    
def get_connection_user(username, password):
    validation_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=129.158.255.133;"
        "PORT=1433;"         
        "DATABASE=PuntoDeVenta;" 
        f"UID={username};"
        f"PWD={password};"
        "TrustServerCertificate=yes;"
    )

    conn = None
    try:
        conn = pyodbc.connect(validation_string)
        return True
        
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        
        if '28000' in sqlstate:
            messagebox.showerror("Error de Autenticación", 
                                 "Usuario o contraseña incorrectos.")
        else:
            messagebox.showerror("Error de Conexión", 
                                 f"No se pudo conectar al servidor: {ex}")
        return False
        
    finally:
        if conn:
            conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
