import conexion_db as db
import tkinter as tk
from tkinter import ttk, messagebox

class Sucursales:
    def __init__(self, master_widget):
        self.id_suc = tk.StringVar()
        self.nombre_suc = tk.StringVar()
        self.folio_suc = tk.StringVar()
        # ---------------- INTERFAZ ----------------
        
        # --- INPUT DE DATOS --
        form_frame = ttk.LabelFrame(master_widget, text="Datos de la Sucursal")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Id:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.id_suc).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.folio_suc).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Folio:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.folio_suc).grid(row=2, column=1, padx=5, pady=5)

        # --- BOTONES DE ESTADO ---
        btn_estados = ttk.Frame(master_widget)
        btn_estados.pack(pady=5)
        ttk.Button(btn_estados, text="Alta", command=self.alta_sucursal).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_estados, text="Modificación", command=self.modificar_Sucursal).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_estados, text="Baja", command=self.baja_sucursal).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_estados, text="Limpiar Campos", command=self.limpiar_campos).pack(side=tk.LEFT, padx=5)

        # --- TABLA ---
        tree_frame = ttk.Frame(master_widget)
        tree_frame.pack(padx=10, pady=10, fill="both", expand=True)
        # - IDENTIFICADORES INTERNOS
        column_ids = ("idSucursal", "nombre", "folioVentaActual")
        self.tree = ttk.Treeview(tree_frame, columns=column_ids, show="headings")
        # - CONFIGURACION DE ENCABEZADOS
        self.tree.heading("idSucursal", text="Id")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("folioVentaActual", text="Folio")
        # - CONFIGURACION DE COLUMNAS
        self.tree.column("idSucursal", width=50, anchor=tk.CENTER)
        self.tree.column("nombre", width=200)
        self.tree.column("folioVentaActual", width=200)
        # - SCROLLBAR
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        # - CARGA DE DATOS
        self.actualizar_Tabla()

    def obtener_Sucursales():
        conn = db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT idSucursal, nombre, folioVentaActual FROM Sucursal")
                records = cursor.fetchall()
                return records
            except Exception as e:
                messagebox.showerror("Error de consulta en Sucursal", f"Error al obtener Sucursal: {e}")
            finally:
                conn.close()
        return []

    def actualizar_Tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
        records = obtener_Sucursales()
        
        for row in records:
            valores_como_tupla = tuple(row)
            self.tree.insert("", tk.END, values=valores_como_tupla)

# ---------------- ESTADOS ----------------

    def alta_sucursal(self):
        nombre = self.nombre_suc.get()
        folio = self.folio_suc.get()

        if nombre:
            agregar_Sucursal(nombre, folio)
            self.actualizar_Tabla()
            self.limpiar_campos()
        else:
            messagebox.showwarning("Campo Vacío", "El nombre es obligatorio.") 

    def baja_sucursal(self):
        nombre = self.nombre_suc.get()
        if not nombre:
            messagebox.showwarning("Sin Selección", "Selecciona un usuario de la lista para eliminar.")
            return
    
        if messagebox.askyesno("Confirmar Baja", f"¿Estás seguro de que deseas eliminar a la sucursal con nombre: {nombre}?"):
            borrar_Sucursal(nombre)
            self.actualizar_Tabla()
            self.limpiar_campos()

    def modificar_Sucursal(self):
        nombre = self.nombre_suc.get()
        if not nombre:
            messagebox.showwarning("Sin Selección", "Selecciona una sucursal de la lista para modificar.")
            return
            
        folio = self.folio_suc()

        if nombre:
            actualizar_Sucursal(nombre, folio)
            self.actualizar_Tabla()
            self.limpiar_campos()
        else:
            messagebox.showwarning("Campo Vacío", "El nombre es obligatorio.")

    def limpiar_campos(self):
        self.nombre_suc.set("")
        self.folio_suc.set("")
        self.tree.selection_remove(self.tree.focus()) 

def obtener_Sucursales():
    conn = db.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT idSucursal, nombre, folioVentaActual FROM SUCURSAL")
            records = cursor.fetchall()
            return records
        except Exception as e:
            messagebox.showerror("Error de consulta en Sucursal", f"Error al obtener Sucursal: {e}")
        finally:
            conn.close()
    return []

def agregar_Sucursal(nombre, folio):
    conn = db.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Sucursal (nombre, folioVentaActual) VALUES (?, ?)", (nombre, folio))
            conn.commit()
            messagebox.showinfo("Éxito", "Sucursal agregada correctamente.")
        except Exception as e:
            messagebox.showerror("Error de Alta", f"Error al agregar Sucursal: {e}")
        finally:
            conn.close()

def borrar_Sucursal(nombre):
    conn = db.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Sucursal WHERE nombre = ?", (nombre))
            conn.commit()
            messagebox.showinfo("Éxito", "Sucursal eliminada correctamente.")
        except Exception as e:
            messagebox.showerror("Error de Baja", f"Error al eliminar sucursal: {e}")
        finally:
            conn.close()

def actualizar_Sucursal(nombre, folio):
    conn = db.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE Sucursal SET nombre = ?, folioVentaActual = ? WHERE nombre = ?", (nombre, folio))
            conn.commit()
            messagebox.showinfo("Éxito", "Sucursal actualizado correctamente.")
        except Exception as e:
            messagebox.showerror("Error de Modificación", f"Error al actualizar sucursal: {e}")
        finally:
            conn.close()