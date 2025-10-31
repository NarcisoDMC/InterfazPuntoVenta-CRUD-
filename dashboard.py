import conexion_db as db
import tkinter as tk
from tkinter import ttk, messagebox

class Dashboard:
    def __init__(self, root):

        self.root = root
        self.root.title("Gestor de Supermercado")
        self.center_window()

        # LETRA ESTILO
        style = ttk.Style()
        style.configure("GrandeDerecha.TLabel", font=("Arial", 16))

        folio_a_mostrar = obtener_siguiente_folio()
        self.folio_dinamico = tk.StringVar()
        self.folio_dinamico.set(f"Folio: {folio_a_mostrar}")

        # INPUTS
        self.producto = tk.StringVar()
        self.cantidad = tk.StringVar()

        lab_folio = ttk.Label(self.root, textvariable=self.folio_dinamico, style="GrandeDerecha.TLabel")
        lab_folio.pack(side=tk.TOP, fill='x', padx=20, pady=10, anchor=tk.W)

        form_frame = ttk.LabelFrame(root, text="Carrito")
        form_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(form_frame, text="Producto: ").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.producto).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Cantidad: ").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.cantidad).grid(row=1, column=1, padx=5, pady=5)

        # TABLA
        tree_frame = ttk.Frame(root)
        tree_frame.pack(padx=50, pady=30, fill="both", expand=True)
        # - IDENTIFICADORES INTERNOS
        column_ids = ("claveProducto","descProd", "cantidad", "precio")
        self.tree = ttk.Treeview(tree_frame, columns=column_ids, show="headings")
        # - CONFIGURACION DE ENCABEZADOS
        self.tree.heading("claveProducto", text="Clave")
        self.tree.heading("descProd", text="Producto")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("precio", text="Precio")
        # - CONFIGURACION DE COLUMNAS
        self.tree.column("claveProducto", width=50, anchor=tk.CENTER)
        self.tree.column("descProd", width=50, anchor=tk.CENTER)
        self.tree.column("cantidad", width=200, anchor=tk.CENTER)
        self.tree.column("precio", width=200, anchor=tk.CENTER)
        # - SCROLLBAR
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        # - CARGA DE DATOS
        self.actualizar_Tabla()

    def actualizar_Tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        records = obtener_detalle_venta()
            
        for row in records:
            valores_como_tupla = tuple(row)
            self.tree.insert("", tk.END, values=valores_como_tupla) 

    def center_window(self):
        window_width = 950  
        window_height = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')   

def obtener_detalle_venta():
    conn = db.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DV.claveProducto, P.descProd, DV.cantidad, DV.precio FROM DetalleVenta AS DV INNER JOIN Producto AS P ON DV.claveProducto = P.claveProducto")
            records = cursor.fetchall()
            return records
        except Exception as e:
            messagebox.showerror("Error de consulta en Detalle Venta", f"Error al obtener Detalle de la venta: {e}")
        finally:
            conn.close()
    return []

def obtener_siguiente_folio():
    conn = db.get_connection()
    siguiente_folio = 1
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(folioVentaActual) FROM Sucursal WHERE idSucursal = 1;") 
            resultado = cursor.fetchone()
            if resultado and resultado[0] is not None:
                siguiente_folio = resultado[0]
            
        except Exception as e:
            messagebox.showerror("Error de Folio", f"Error al obtener el folio de Sucursal: {e}")
        finally:
            conn.close()
            
    return siguiente_folio


if __name__ == "__main__":
    root = tk.Tk()
    venta = Dashboard(root)
    root.mainloop()