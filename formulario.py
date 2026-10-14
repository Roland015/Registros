import tkinter as tk
from tkinter import messagebox,scrolledtext, ttk
import mysql.connector


# primera clase
class FormularioRegistro:
    def __init__(self, root):
        self.root = root
        self.root.title("Titulo Principal")
        self.root.config(bg='#e6f2f2')
        self.root.resizable(False,False)
        self.lbl_estado = None

        ancho = 760
        alto = 680
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

        # TITULO DEL FORMULaRIO
        titulo_frame = tk.Frame(self.root, bg="#D6D8D8",bd=2, relief='groove')
        titulo_frame.place(relx=0.5, y=10, anchor='n', width=660, height=60)

        lbl_titulo = tk.Label(titulo_frame, text='FORMULARIO DE REGISTROS DE USUARIOS',
                              bg='#D6D8D8', fg='black', font=('arial',16,'bold'))
        lbl_titulo.pack(expand=True)

        # panel principal de los campos
        self.crear_campos()

        # Botones de acciones
        self.crear_botones()

        # areas de resultados / log
        self.crear_area_resultados()

    # ============================================================================
    # Funcion crear campos
    # ============================================================================
    def crear_campos(self):
        campos_frame = tk.Frame(self.root, bg='#D6D8D8', bd=2, relief='ridge')
        campos_frame.place(relx=0.5, y=100, anchor='n', width=560, height=350)
        self.entradas = {}
        labels = ["Nombre","Apellido","Edad","Nacionalidad","Email","Telefono","Direccion"]
        nacionalidades = ["Argentina", "Bolivia", "Chile", "Colombia", "Costa Rica",
                          "Ecuador", "España", "Guatemala", "México", "Perú",
                          "Puerto Rico", "República Dominicana", "Uruguay", "Venezuela"]

        x_label = 70
        x_entry = 220
        y_pos = 20
        # aplicamos el bucle for
        for campo in labels:
            lbl = tk.Label(campos_frame, text=campo, bg='#D6D8D8', fg='black', font=('arial',11,'bold'))
            lbl.place(x=x_label, y=y_pos)

            if campo == "Nacionalidad":
                entry = ttk.Combobox(campos_frame, values=nacionalidades, state='readonly', font=('arial',10,'bold'), width=25)
                entry.place(x=x_entry, y=y_pos)
                entry.set('')
            else:
                # campos de textos
                entry = tk.Entry(campos_frame, font=('arial',11,'bold'),bg='white', fg='#333', relief='solid', bd=1, width=30)
                entry.place(x=x_entry, y=y_pos)

            self.entradas[campo] = entry
            y_pos += 42
    # ============================================================================
    # Funcion crear Botones
    # ============================================================================
    def crear_botones(self):
        centro_x = 380
        separacion = 150

        btn_guardar = tk.Button(self.root, text='Guardar', bg="#121312", fg='white',
                               font=('arial',11,'bold'), width=12, relief='raised', command=self.guardar_datos)
        btn_guardar.place(x=centro_x - separacion, y=470)

        btn_limpiar = tk.Button(self.root, text='Limpiar', bg='#121312', fg='white',
                                       font=('arial',11,'bold'), width=12, relief='raised', command=self.limpiar_campos)
        btn_limpiar.place(x=centro_x, y=470)

        btn_salir = tk.Button(self.root, text='Salir', bg='#121312', fg='white',
                                       font=('arial',11,'bold'), width=12, relief='raised', command=self.root.quit)
        btn_salir.place(x=centro_x + separacion, y=470)
    # ============================================================================
    # Funcion crear area resultados
    # ============================================================================
    def crear_area_resultados(self):
        res_frame = tk.Frame(self.root, bg='#d1e7e7', bd=2, relief='ridge')
        res_frame.place(relx=0.5, y=520, anchor='n', width=670, height=130)
        # label
        lbl_res = tk.Label(res_frame, text='Resultado Guardado/Log:',bg='#d1e7e7', fg="#0e0f0f", font=('arial',12,'bold'))
        lbl_res.pack(anchor='center', padx=10, pady=2)
        # textos de resultados
        self.txt_resultados = scrolledtext.ScrolledText(res_frame, font=('arial',10), bg='white', fg='#333', height=5)
        self.txt_resultados.pack(fill='both', padx=10, pady=5, expand=True)
    # ============================================================================
    # Funcion para obtner la conexion
    # ============================================================================
    def obtener_conexion(self):
        try:
            conexion = mysql.connector.connect(
                host = 'localhost',
                user = 'root',
                password = 'keyla016',
                database = 'sis_usuarios'
            )
            return conexion
        except mysql.connector.Error as err:
            messagebox.showerror("Error en la Conexion", f"No se puede conectar a MySQL Workbench:\n{err}")
            return None
    # ============================================================================
    # Funcion para probar la conexion
    # ============================================================================
    def probar_conexion(self):
        conexion = self.obtener_conexion()
        if conexion:
            if self.lbl_estado is not None:
                self.lbl_estado.config(text="Conexion Establecida", fg='#006600')
            messagebox.showinfo("Conexion Exitosa", "Se ha establecido la conexion con MySQL Workbench.")
            conexion.close()
        else:
            if self.lbl_estado is not None:
                self.lbl_estado.config(text="Conexion Fallida", fg='#cc0000')
            messagebox.showerror("Error de Conexion", "No se pudo establecer la conexion con MySQL Workbench.")
    # ============================================================================
    # Funcion para guardar datos
    # ============================================================================
    def guardar_datos(self):
        # obtenemos los datos de los campos
        datos = {campo: entry.get().strip() for campo, entry in self.entradas.items()}
        # validamos que no esten vacios
        if any(not valor for valor in datos.values()):
            messagebox.showwarning("Campos Vacios", "Por favor, complete todos los campos antes de guardar.")
            return

        conexion = self.obtener_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                sql = "INSERT INTO usuarios (nombre, apellido, edad, nacionalidad, email, telefono, direccion) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                valores = (datos["Nombre"], datos["Apellido"], datos["Edad"], datos["Nacionalidad"],
                           datos["Email"], datos["Telefono"], datos["Direccion"])
                cursor.execute(sql, valores)
                conexion.commit()
                self.txt_resultados.insert(tk.END, f"Datos guardados correctamente: {valores}\n")
                messagebox.showinfo("Registro Exitoso", "Los datos se han guardado correctamente en la base de datos.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error al Guardar", f"No se pudo guardar los datos:\n{err}")
            finally:
                cursor.close()
                conexion.close()
    # ============================================================================
    # Funcion para limpiar campos
    # ============================================================================
    def limpiar_campos(self):
        for entry in self.entradas.values():
            if hasattr(entry, 'set'):
                entry.set('')
            else:
                entry.delete(0, tk.END)
        self.txt_resultados.delete('1.0', tk.END)
        messagebox.showinfo("Campos Limpiados", "Todos los campos han sido limpiados.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FormularioRegistro(root)
    root.mainloop()  # cierre
 