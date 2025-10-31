import conexion_db as db
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc 

class Dashboard:
    def __init__(self, root):

        self.root = root
        self.root.title("Gestor de Supermercado")
        self.center_window()

        self.carrito = [] 
        self.total_venta = tk.DoubleVar(value=0.0) 
        self.total_display = tk.StringVar(value="Total: $0.00") 

        # LETRA ESTILO
        style = ttk.Style()
        style.configure("GrandeDerecha.TLabel", font=("Arial", 16))
        style.configure("Total.TLabel", font=("Arial", 14, "bold"), foreground="blue")

        folio_a_mostrar = obtener_siguiente_folio()
        self.folio_dinamico = tk.StringVar()
        self.folio_dinamico.set(f"Siguiente Folio: {folio_a_mostrar}")

        # INPUTS
        self.producto_clave = tk.StringVar() 
        self.cantidad = tk.StringVar()

        lab_folio = ttk.Label(self.root, textvariable=self.folio_dinamico, style="GrandeDerecha.TLabel")
        lab_folio.pack(side=tk.TOP, fill='x', padx=20, pady=10, anchor=tk.W)

        form_frame = ttk.LabelFrame(root, text="Agregar Producto")
        form_frame.pack(padx=10, pady=10, fill="x")

        # Labels y Entries para agregar productos
        ttk.Label(form_frame, text="Clave Producto: ").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_producto = ttk.Entry(form_frame, textvariable=self.producto_clave, width=15)
        self.entry_producto.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Cantidad: ").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_cantidad = ttk.Entry(form_frame, textvariable=self.cantidad, width=15)
        self.entry_cantidad.grid(row=0, column=3, padx=5, pady=5)
        
        self.btn_agregar = ttk.Button(form_frame, text="Agregar al Carrito", command=self.agregar_al_carrito)
        self.btn_agregar.grid(row=0, column=4, padx=10, pady=5)
        
        self.entry_producto.focus()
        self.entry_producto.bind('<Return>', lambda e: self.entry_cantidad.focus())
        self.entry_cantidad.bind('<Return>', lambda e: self.agregar_al_carrito())


        # TABLA (Carrito)
        tree_frame = ttk.Frame(root)
        tree_frame.pack(padx=10, pady=10, fill="both", expand=True) 
        
        column_ids = ("claveProducto","descProd", "cantidad", "precio_unit", "subtotal") 
        self.tree = ttk.Treeview(tree_frame, columns=column_ids, show="headings")
        
        self.tree.heading("claveProducto", text="Clave")
        self.tree.heading("descProd", text="Producto")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("precio_unit", text="Precio Unit.")
        self.tree.heading("subtotal", text="Subtotal") 
        
        self.tree.column("claveProducto", width=50, anchor=tk.CENTER)
        self.tree.column("descProd", width=200)
        self.tree.column("cantidad", width=80, anchor=tk.CENTER)
        self.tree.column("precio_unit", width=100, anchor=tk.E)
        self.tree.column("subtotal", width=100, anchor=tk.E) 
        
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        
        # Frame para Total y botones de Venta
        total_frame = ttk.Frame(root)
        total_frame.pack(fill="x", padx=10, pady=10)
        
        self.lbl_total = ttk.Label(total_frame, textvariable=self.total_display, style="Total.TLabel")
        self.lbl_total.pack(side=tk.LEFT, padx=10)

        # Botones de acción (empaquetados de derecha a izquierda)
        self.btn_registrar = ttk.Button(total_frame, text="Registrar Venta", command=self.realizar_venta)
        self.btn_registrar.pack(side=tk.RIGHT, padx=5)
        
        # Boton para cancelar venta
        self.btn_cancelar = ttk.Button(total_frame, text="Cancelar Venta", command=self.limpiar_venta)
        self.btn_cancelar.pack(side=tk.RIGHT, padx=5)

        # Boton para quitar producto
        self.btn_quitar = ttk.Button(total_frame, text="Quitar Producto", command=self.eliminar_del_carrito)
        self.btn_quitar.pack(side=tk.RIGHT, padx=5)


    def agregar_al_carrito(self):
        try:
            clave = int(self.producto_clave.get())
            cantidad = int(self.cantidad.get())
            if cantidad <= 0:
                messagebox.showwarning("Dato Inválido", "La cantidad debe ser mayor a cero.")
                return
        except ValueError:
            messagebox.showwarning("Dato Inválido", "La clave y la cantidad deben ser números.")
            return

        producto_info = obtener_producto_por_clave(clave)
        if not producto_info:
            messagebox.showerror("No Encontrado", f"El producto con clave {clave} no existe.")
            return

        desc, precio, stock = producto_info

        if cantidad > stock:
            messagebox.showwarning("Stock Insuficiente", f"Solo quedan {stock} unidades de '{desc}'.")
            return
            
        subtotal = cantidad * precio
        item_carrito = (clave, desc, cantidad, precio, subtotal)
        
        self.carrito.append(item_carrito)
        self.actualizar_treeview_carrito()
        self.actualizar_total()

        self.producto_clave.set("")
        self.cantidad.set("")
        self.entry_producto.focus()

    def actualizar_treeview_carrito(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for item in self.carrito:
            item_formateado = (
                item[0], 
                item[1], 
                item[2], 
                f"${item[3]:.2f}", 
                f"${item[4]:.2f}"
            )
            self.tree.insert("", tk.END, values=item_formateado) 

    def actualizar_total(self):
        total = sum(item[4] for item in self.carrito) # Suma los subtotales
        self.total_venta.set(total) 
        self.total_display.set(f"Total: ${total:.2f}") 

    def limpiar_venta(self):
        if not self.carrito:
            return
            
        if messagebox.askyesno("Confirmar", "¿Desea limpiar el carrito actual?"):
            self.carrito.clear()
            self.actualizar_treeview_carrito()
            self.actualizar_total()
            
            nuevo_folio = obtener_siguiente_folio()
            self.folio_dinamico.set(f"Siguiente Folio: {nuevo_folio}")
            
            self.entry_producto.focus()
            
    # --- FUNCIÓN PARA ELIMINAR UN PRODUCTO DEL CARRITO ---
    def eliminar_del_carrito(self):
        """
        Quita el producto seleccionado en el Treeview del carrito.
        """
        # 1. Obtener el item seleccionado (esto da un ID interno de tkinter, ej: 'I001')
        selected_item_id = self.tree.focus() 

        if not selected_item_id:
            messagebox.showwarning("Nada Seleccionado", "Por favor, selecciona un producto de la lista para quitarlo.")
            return

        # 2. Obtener el índice numérico (0, 1, 2...) de ese item
        try:
            item_index = self.tree.index(selected_item_id)
        
            # 3. Eliminar ese item de la lista de *datos* (self.carrito)
            self.carrito.pop(item_index)
        
            # 4. Actualizar la vista (Treeview)
            self.actualizar_treeview_carrito()
            
            # 5. Actualizar el total
            self.actualizar_total()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo quitar el item: {e}")

    #Función para registrar la venta en la base de datos con manejo de transacciones
    def realizar_venta(self):
        if not self.carrito:
            messagebox.showwarning("Carrito Vacío", "Agregue al menos un producto para registrar la venta.")
            return

        if not messagebox.askyesno("Confirmar Venta", f"¿Desea registrar esta venta?\n{self.total_display.get()}"):
            return
            
        conn = None
        try:
            conn = db.get_connection()
            if not conn:
                messagebox.showerror("Error de Conexión", "No se pudo conectar a la BD para la transacción.")
                return

            # --- INICIO DE LA TRANSACCIÓN ---
            conn.autocommit = False
            cursor = conn.cursor()
            
            id_sucursal_actual = 1

            # 1. Obtener el nuevo folio (Bloquea la fila)
            cursor.execute("SELECT folioVentaActual + 1 FROM Sucursal WITH (UPDLOCK) WHERE idSucursal = ?", (id_sucursal_actual))
            resultado_folio = cursor.fetchone()
            if not resultado_folio:
                raise Exception(f"No se encontró la sucursal {id_sucursal_actual}")
            
            nuevo_folio = resultado_folio[0]
            total_calculado = self.total_venta.get() 

            # 2. Registrar el encabezado de la Venta
            cursor.execute("INSERT INTO Venta (idVenta, idSucursal, total) VALUES (?, ?, ?)", 
                           (nuevo_folio, id_sucursal_actual, total_calculado))

            # 3. Registrar los detalles y actualizar stock
            for item in self.carrito:
                clave, desc, cant, precio, subtotal = item
                
                cursor.execute("INSERT INTO DetalleVenta (idVenta, claveProducto, cantidad, precio) VALUES (?, ?, ?, ?)",
                               (nuevo_folio, clave, cant, precio))
                
                cursor.execute("UPDATE Producto SET stock = stock - ? WHERE claveProducto = ?", (cant, clave))

            # 4. Actualizar el folio en la tabla Sucursal
            cursor.execute("UPDATE Sucursal SET folioVentaActual = ? WHERE idSucursal = ?", 
                           (nuevo_folio, id_sucursal_actual))

            # 5. Si todo salió bien, confirmar todos los cambios
            conn.commit() # --- COMMIT DE LA TRANSACCIÓN ---
            
            messagebox.showinfo("Éxito", f"Venta {nuevo_folio} registrada correctamente.")
            self.limpiar_venta() 
            self.folio_dinamico.set(f"Siguiente Folio: {nuevo_folio + 1}")

        except pyodbc.Error as ex:
            # 6. Si algo falló, deshacer TODOS los cambios
            sqlstate = ex.args[0]
            if conn:
                conn.rollback() # --- ROLLBACK DE LA TRANSACCIÓN ---
            
            if "CK__Producto__stock" in str(ex):
                 messagebox.showerror("Error de Stock", "La venta no pudo completarse. El stock de un producto no es suficiente (quizás alguien más compró al mismo tiempo).")
            else:
                 messagebox.showerror("Error de Transacción", f"No se pudo registrar la venta. Se revirtieron los cambios.\nError: {ex}")
        
        except Exception as e:
            if conn:
                conn.rollback() # --- ROLLBACK DE LA TRANSACCIÓN ---
            messagebox.showerror("Error Inesperado", f"Ocurrió un error: {e}")

        finally:
            # 7. Siempre cerrar la conexión y restaurar el autocommit
            if conn:
                conn.autocommit = True
                conn.close()


    def center_window(self):
        window_width = 800  
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')   

# Función para obtener el siguiente folio de venta
def obtener_siguiente_folio():
    conn = db.get_connection()
    siguiente_folio = 1 
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT folioVentaActual FROM Sucursal WHERE idSucursal = 1;") 
            resultado = cursor.fetchone()
            if resultado and resultado[0] is not None:
                siguiente_folio = resultado[0] + 1 
            
        except Exception as e:
            messagebox.showerror("Error de Folio", f"Error al obtener el folio de Sucursal: {e}")
        finally:
            conn.close()
            
    return siguiente_folio

# Función para obtener información del producto por su clave
def obtener_producto_por_clave(clave):
    conn = db.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT descProd, precio, stock FROM Producto WHERE claveProducto = ?", (clave))
            record = cursor.fetchone()
            return record 
        except Exception as e:
            messagebox.showerror("Error de consulta", f"Error al buscar producto: {e}")
        finally:
            conn.close()
    return None


if __name__ == "__main__":
    root = tk.Tk()
    venta = Dashboard(root)
    root.mainloop()