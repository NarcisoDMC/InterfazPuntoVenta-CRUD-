import tkinter as tk
from tkinter import ttk, messagebox
from sucursal import Sucursales

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Supermercado")
        self.center_window()

        self.boton_suc = ttk.Frame(root)
        self.boton_cerrar_sesion = ttk.Frame(root)
        self.boton_suc.pack(pady=5)

        ttk.Button(self.boton_suc, text="Sucursales", command=self.abrir_sucursal).pack(side=tk.LEFT, padx=5)      
        ttk.Button(root, text="Cerrar Sesión", command=self.logout).pack(pady=20)

    def abrir_sucursal(self):
        self.boton_suc.pack_forget()
        self.boton_cerrar_sesion.pack_forget()
        instancia_sucursal = Sucursales(self.root)

    def logout(self):
        self.root.destroy()

    def center_window(self):
        window_width = 950  
        window_height = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

if __name__ == "__main__":
    root = tk.Tk()
    dashboard = Dashboard(root)
    root.mainloop()