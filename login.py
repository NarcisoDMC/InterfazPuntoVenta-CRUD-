import tkinter as tk
from tkinter import ttk, messagebox
import conexion_db as db
from dashboard import Dashboard

class LoginApp:
    def __init__(self, master):
        self.master = master
        master.title("Login de Usuario")
        master.resizable(False, False)
        self.center_window()

        self.nombre_usuario = tk.StringVar()
        self.contrasena = tk.StringVar()

        # --- LOGIN INTERFAZ ---
        main_frame = ttk.Frame(master, padding=10)
        main_frame.pack(padx=15, pady=15, fill="both", expand=True)

        ttk.Label(main_frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.user_entry = ttk.Entry(main_frame, textvariable=self.nombre_usuario, width=25)
        self.user_entry.grid(row=0, column=1, padx=5, pady=5)
        self.user_entry.focus()

        ttk.Label(main_frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.pass_entry = ttk.Entry(main_frame, textvariable=self.contrasena, show="*", width=25)
        self.pass_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Button(main_frame, text="Iniciar Sesión", command=self.handle_login).grid(row=2, column=0, columnspan=2, pady=10)
        master.bind('<Return>', lambda event: self.handle_login())

    def handle_login(self):
        user = self.nombre_usuario.get().strip()
        pwd = self.contrasena.get()

        if not user or not pwd:
            messagebox.showwarning("Faltan Datos", "Por favor, introduce tu usuario y contraseña.")
            return

        if db.get_connection_user(user, pwd):
            messagebox.showinfo("Éxito", f"Bienvenido, {user}. Inicio de sesión exitoso.")
            self.master.destroy()
            app_root = tk.Tk()
            aplicacion_principal = Dashboard(app_root)
            app_root.mainloop()

        else:
            self.contrasena.set("") 
            self.pass_entry.focus() 

    def center_window(self):
        window_width = 300  
        window_height = 200 
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

if __name__ == '__main__':
    root = tk.Tk()
    app_login = LoginApp(root)
    root.mainloop()