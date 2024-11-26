import tkinter as tk
from tkinter import  messagebox
import sqlite3

# German Stanely Campos Sosa: trabaje la creacion y la conexion de base de datos 
def inicializar_db():
    conn = sqlite3.connect("usuarios.db")
    cursor = conn.cursor()

    # Esta es la tabla para los usuarios en la base de datos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            correo TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    # Esta es la tabla para los boletos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            aerolinea TEXT NOT NULL,
            origen TEXT NOT NULL,
            destino TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora_salida TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

#cg22036 ederson wigberto chevez galindo yo aporte en las clases y herencias 
# Clase padre
class Transporte:
    def __init__(self, nombre):
        self._nombre = nombre


# Clase que hereda
class Aerolinea(Transporte):
    def __init__(self, nombre):
        super().__init__(nombre)
        self._vuelos = []

    def agregar_vuelo(self, vuelo):
        self._vuelos.append(vuelo)


# Clase Vuelo que hereda de Transporte
class Vuelo(Transporte):
    def __init__(self, origen, destino, fecha, hora_salida, precio, asientos_disponibles):
        super().__init__(origen)
        self._destino = destino
        self._fecha = fecha
        self._hora_salida = hora_salida
        self._precio = precio
        self._asientos_disponibles = asientos_disponibles

    def reservar_asiento(self):
        if self._asientos_disponibles > 0:
            self._asientos_disponibles -= 1
            return True
        return False


# Ventana principal del sistema de boletos
class InterfazVentaBoletos:
    def __init__(self, aerolineas, usuario):
        self.usuario = usuario
        self.aerolineas = aerolineas
        self.vuelos_map = {}  # aqui Inicia el vuelos_map aquí
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Venta de Boletos")
        self.ventana.geometry("600x400")

        # Listbox para aerolíneas
        tk.Label(self.ventana, text="Aerolíneas:").pack()
        self.lista_aerolineas = tk.Listbox(self.ventana)
        self.lista_aerolineas.pack()

        # Listbox para vuelos
        tk.Label(self.ventana, text="Vuelos:").pack()
        self.lista_vuelos = tk.Listbox(self.ventana)
        self.lista_vuelos.pack()

        # Botones
        tk.Button(self.ventana, text="Mostrar Vuelos", command=self.mostrar_vuelos).pack()
        tk.Button(self.ventana, text="Comprar Boleto", command=self.comprar_boleto).pack()

        # Detalles de vuelo
        tk.Label(self.ventana, text="Detalles del vuelo:").pack()
        self.text_detalles = tk.Text(self.ventana, height=8)
        self.text_detalles.pack()

        for aerolinea in self.aerolineas:
            self.lista_aerolineas.insert(tk.END, aerolinea._nombre)

        self.ventana.mainloop()

    def mostrar_vuelos(self):
        self.lista_vuelos.delete(0, tk.END)
        self.text_detalles.delete("1.0", tk.END)
        try:
            index = self.lista_aerolineas.curselection()[0]
            aerolinea = self.aerolineas[index]
            
            # Borre el vuelos_map antes de insertar nuevos datos
            self.vuelos_map.clear()

            for idx, vuelo in enumerate(aerolinea._vuelos):
                info = (f"{vuelo._nombre} -> {vuelo._destino} "
                        f"(${vuelo._precio}) "
                        f"Asientos: {vuelo._asientos_disponibles}")
                self.lista_vuelos.insert(tk.END, info)
                self.vuelos_map[idx] = vuelo  # Almacenar el objeto Vuelo con su index
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una aerolínea.")

    def comprar_boleto(self):
        # Comprueba si se ha seleccionado un vuelo en el cuadro de lista de vuelos
        selection = self.lista_vuelos.curselection()
        
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un vuelo.")
            return

       # Obtiene el index del vuelo seleccionado
        flight_index = selection[0]
        
        # Recupera el objeto Vuelo utilizando el index de  vuelos_map
        vuelo_seleccionado = self.vuelos_map.get(flight_index)
        
        if vuelo_seleccionado:
            #  reservar asiento
            if vuelo_seleccionado.reservar_asiento():
                # Registrar la compra (insertandolo en la tabla de compras)
                self.registrar_compra(vuelo_seleccionado, vuelo_seleccionado._nombre)
                messagebox.showinfo("Compra exitosa", f"¡Compra exitosa! Has adquirido el boleto de {vuelo_seleccionado._nombre}.")
                self.actualizar_detalles_vuelo(vuelo_seleccionado)
            else:
                messagebox.showwarning("Advertencia", "No hay asientos disponibles para este vuelo.")
        else:
            messagebox.showwarning("Advertencia", "Hubo un problema con la selección del vuelo.")

    def registrar_compra(self, vuelo, aerolinea_nombre):
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO compras (usuario, aerolinea, origen, destino, fecha, hora_salida, precio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.usuario, aerolinea_nombre, vuelo._nombre, vuelo._destino, vuelo._fecha, vuelo._hora_salida, vuelo._precio))
        conn.commit()
        conn.close()

    def actualizar_detalles_vuelo(self, vuelo):
        """ Update the available seats and show updated flight details in the GUI. """
        self.text_detalles.delete("1.0", tk.END)
        detalles = (
            f"Nombre del vuelo: {vuelo._nombre}\n"
            f"Origen: {vuelo._nombre}\n"
            f"Destino: {vuelo._destino}\n"
            f"Fecha: {vuelo._fecha}\n"
            f"Hora de salida: {vuelo._hora_salida}\n"
            f"Precio: ${vuelo._precio}\n"
            f"Asientos disponibles: {vuelo._asientos_disponibles}"
        )
        self.text_detalles.insert(tk.END, detalles)


# Muestra la ventana de inicio de sesión
class Login:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Inicio de Sesión")
        self.ventana.geometry("300x200")

        tk.Label(self.ventana, text="Usuario:").pack()
        self.entry_usuario = tk.Entry(self.ventana)
        self.entry_usuario.pack()

        tk.Label(self.ventana, text="Contraseña:").pack()
        self.entry_contraseña = tk.Entry(self.ventana, show="*")
        self.entry_contraseña.pack()

        tk.Button(self.ventana, text="Iniciar Sesión", command=self.iniciar_sesion).pack()
        tk.Button(self.ventana, text="Registrarse", command=self.registrarse).pack()
        self.ventana.mainloop()

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        contraseña = self.entry_contraseña.get()
        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (usuario, contraseña))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            self.ventana.destroy()
            self.abrir_sistema_boletos(usuario)
        else:
            messagebox.showerror("Error", "Credenciales inválidas.")

    def registrarse(self):
        # Abrir nueva ventana de registro
        self.ventana_registro = tk.Tk()
        self.ventana_registro.title("Registro de Usuario")
        self.ventana_registro.geometry("300x250")

        tk.Label(self.ventana_registro, text="Correo:").pack()
        self.entry_correo = tk.Entry(self.ventana_registro)
        self.entry_correo.pack()

        tk.Label(self.ventana_registro, text="Usuario:").pack()
        self.entry_usuario_registro = tk.Entry(self.ventana_registro)
        self.entry_usuario_registro.pack()

        tk.Label(self.ventana_registro, text="Contraseña:").pack()
        self.entry_contraseña_registro = tk.Entry(self.ventana_registro, show="*")
        self.entry_contraseña_registro.pack()

        tk.Button(self.ventana_registro, text="Registrar", command=self.registrar_usuario).pack()

    def registrar_usuario(self):
        correo = self.entry_correo.get()
        usuario = self.entry_usuario_registro.get()
        contraseña = self.entry_contraseña_registro.get()

        if not correo or not usuario or not contraseña:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        conn = sqlite3.connect("usuarios.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO usuarios (correo, username, password) VALUES (?, ?, ?)", (correo, usuario, contraseña))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.ventana_registro.destroy()  # Cierra la ventana de registro
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El usuario ya existe.")
        finally:
            conn.close()

    # Muestra el sistema de boletos
    def abrir_sistema_boletos(self, usuario):
        aerolinea1 = Aerolinea("AeroMex")
        aerolinea1.agregar_vuelo(Vuelo("CDMX", "Madrid", "2024-12-15", "15:30", 500, 10))
        aerolinea1.agregar_vuelo(Vuelo("Barcelona", "CDMX", "2024-12-15", "15:30", 500, 10))
        

        aerolinea2 = Aerolinea("Volaris")
        aerolinea2.agregar_vuelo(Vuelo("El Salvador", "New York", "2024-12-01", "18:00", 600, 8))
        aerolinea2.agregar_vuelo(Vuelo("El Salvador", " Puntacana", "2024-11-30", "14:00", 500, 30))
        aerolinea2.agregar_vuelo(Vuelo("washington", " El Salvador", "2024-12-1", "8:00", 600, 30))

        aerolinea3 = Aerolinea("Avianca")
        aerolinea3.agregar_vuelo(Vuelo("Bogotá", "Miami", "2024-11-20", "12:00", 400, 15))
        aerolinea3.agregar_vuelo(Vuelo("El Salvador", "Medellin", "2024-11-28", "12:00", 320, 20))
        aerolinea3.agregar_vuelo(Vuelo("Los Angeles", "El Salvador", "2024-12-15", "10:00", 650, 25))

        aerolinea4 = Aerolinea("United Airlines")
        aerolinea4.agregar_vuelo(Vuelo("Houston", "Tokyo", "2024-11-25", "20:00", 1000, 5))
        aerolinea4.agregar_vuelo(Vuelo("Miami", "Francia", "2024-01-10", "15:00", 1500, 16))
        aerolinea4.agregar_vuelo(Vuelo("Madrid", "El Salvador", "2024-01-02", "8:00", 2500, 18))


        aerolinea5 = Aerolinea("Delta")
        aerolinea5.agregar_vuelo(Vuelo("Los Angeles", "Alaska", "2024-12-01", "12:00", 200, 20))
        aerolinea5.agregar_vuelo(Vuelo("North Carolina", "Vancuver", "2024-12-07", "11:00", 400, 10))



        aerolineas = [aerolinea1, aerolinea2, aerolinea3, aerolinea4]
        InterfazVentaBoletos(aerolineas, usuario)


if __name__ == "__main__":
    inicializar_db()
    Login()
