import tkinter as tk
from tkinter import ttk, messagebox
from sucursal import Sucursales

class Main:
    def __init__(self, root):
        # Frame para botones
        # Boton sucursal
        self.boton_suc = ttk.Frame(root)
        self.boton_suc.pack(pady=5)

        ttk.Button(self.boton_suc, text="Sucursales", command=self.abrir_sucursal).pack(side=tk.LEFT, padx=5) 
    
    def abrir_sucursal(self):
        self.boton_suc.pack_forget()
        instancia_sucursal = Sucursales(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()