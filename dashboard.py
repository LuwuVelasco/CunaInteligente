import tkinter as tk
from tkinter import messagebox, ttk, Canvas, Scrollbar
from PIL import Image, ImageTk
import mysql.connector
import plotly.graph_objs as go
import plotly.io as pio
import threading
import time
import io

id_usuario = None

# Conexión a la base de datos
def conectar_bd():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",  # Cambia al usuario correcto
            password="",  # Cambia a la contraseña correcta
            database="cunainteligente"
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Función de inicio de sesión
def iniciar_sesion(username, password):
    global id_usuario
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_usuario FROM usuario WHERE username=%s AND contrasenia=%s", (username, password))
        usuario = cursor.fetchone()
        conexion.close()
        if usuario:
            id_usuario = usuario[0]
            return True
    return False

# Función para el registro de un nuevo usuario
def registrar_usuario(nombre, apellido_p, apellido_m, username, gmail, password):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuario (nombre, apellidoPaterno, apellidoMaterno, username, gmail, contrasenia) VALUES (%s, %s, %s, %s, %s, %s)",
                       (nombre, apellido_p, apellido_m, username, gmail, password))
        conexion.commit()
        conexion.close()
        return True
    return False

# Ventana de registro de usuario
def ventana_registro():
    def registrar():
        nombre = entry_nombre.get()
        apellido_p = entry_apellido_p.get()
        apellido_m = entry_apellido_m.get()
        username = entry_username.get()
        gmail = entry_gmail.get()
        password = entry_password.get()

        if registrar_usuario(nombre, apellido_p, apellido_m, username, gmail, password):
            messagebox.showinfo("Éxito", "Registro exitoso")
            ventana_registro.destroy()
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario")

    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registro de Usuario")

    tk.Label(ventana_registro, text="Nombre").pack()
    entry_nombre = tk.Entry(ventana_registro)
    entry_nombre.pack()

    tk.Label(ventana_registro, text="Apellido Paterno").pack()
    entry_apellido_p = tk.Entry(ventana_registro)
    entry_apellido_p.pack()

    tk.Label(ventana_registro, text="Apellido Materno").pack()
    entry_apellido_m = tk.Entry(ventana_registro)
    entry_apellido_m.pack()

    tk.Label(ventana_registro, text="Nombre de Usuario").pack()
    entry_username = tk.Entry(ventana_registro)
    entry_username.pack()

    tk.Label(ventana_registro, text="Correo Gmail").pack()
    entry_gmail = tk.Entry(ventana_registro)
    entry_gmail.pack()

    tk.Label(ventana_registro, text="Contraseña").pack()
    entry_password = tk.Entry(ventana_registro, show="*")
    entry_password.pack()

    tk.Button(ventana_registro, text="Registrar", command=registrar).pack()


# Ventana de inicio de sesión
def ventana_inicio():
    def login():
        username = entry_user.get()
        password = entry_pass.get()
        if iniciar_sesion(username, password):
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            seleccionar_bebe()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    ventana = tk.Tk()
    ventana.title("Inicio de Sesión")

    tk.Label(ventana, text="Usuario").pack()
    entry_user = tk.Entry(ventana)
    entry_user.pack()

    tk.Label(ventana, text="Contraseña").pack()
    entry_pass = tk.Entry(ventana, show="*")
    entry_pass.pack()

    tk.Button(ventana, text="Ingresar", command=login).pack()
    tk.Button(ventana, text="Registrarse", command=ventana_registro).pack()
    ventana.mainloop()

# Ventana para selección de bebés
def seleccionar_bebe():
    def cargar_bebes():
        # Limpiar la lista de botones antes de volver a cargar
        for widget in frame_bebes.winfo_children():
            widget.destroy()
        
        # Conectar a la base de datos y obtener bebés del usuario actual
        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_bebe, nombre, apellidoPaterno FROM bebe WHERE usuario_id_usuario=%s", (id_usuario,))
            bebes = cursor.fetchall()
            conexion.close()
            
            # Crear botones para cada bebé registrado
            for bebe in bebes:
                id_bebe, nombre, apellidoPaterno = bebe
                boton_bebe = tk.Button(frame_bebes, text=f"{nombre} {apellidoPaterno}", command=iniciar_dashboard)
                boton_bebe.pack(fill='x')

    def agregar_bebe():
        def registrar_nuevo_bebe():
            nombre = entry_nombre.get()
            apellido_p = entry_apellido_p.get()
            apellido_m = entry_apellido_m.get()
            fecha_nac = entry_fecha_nac.get()

            conexion = conectar_bd()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    "INSERT INTO bebe (nombre, apellidoPaterno, apellidoMaterno, fechaDeNacimiento, usuario_id_usuario) VALUES (%s, %s, %s, %s, %s)",
                    (nombre, apellido_p, apellido_m, fecha_nac, id_usuario)
                )
                conexion.commit()
                conexion.close()
                messagebox.showinfo("Éxito", "Bebé registrado exitosamente")
                ventana_agregar_bebe.destroy()
                cargar_bebes()  # Actualizar lista de bebés

        # Ventana para registrar un nuevo bebé
        ventana_agregar_bebe = tk.Toplevel(ventana_bebe)
        ventana_agregar_bebe.title("Registrar Nuevo Bebé")

        tk.Label(ventana_agregar_bebe, text="Nombre").pack()
        entry_nombre = tk.Entry(ventana_agregar_bebe)
        entry_nombre.pack()

        tk.Label(ventana_agregar_bebe, text="Apellido Paterno").pack()
        entry_apellido_p = tk.Entry(ventana_agregar_bebe)
        entry_apellido_p.pack()

        tk.Label(ventana_agregar_bebe, text="Apellido Materno").pack()
        entry_apellido_m = tk.Entry(ventana_agregar_bebe)
        entry_apellido_m.pack()

        tk.Label(ventana_agregar_bebe, text="Fecha de Nacimiento (AAAA-MM-DD)").pack()
        entry_fecha_nac = tk.Entry(ventana_agregar_bebe)
        entry_fecha_nac.pack()

        tk.Button(ventana_agregar_bebe, text="Registrar", command=registrar_nuevo_bebe).pack()

    # Ventana de selección de bebé
    ventana_bebe = tk.Tk()
    ventana_bebe.title("Seleccionar Bebé")

    # Frame para mostrar la lista de bebés
    frame_bebes = tk.Frame(ventana_bebe)
    frame_bebes.pack(fill='both', expand=True)

    # Cargar los bebés registrados para el usuario actual
    cargar_bebes()

    # Botón para añadir un nuevo bebé
    tk.Button(ventana_bebe, text="Añadir Bebé", command=agregar_bebe).pack()

    ventana_bebe.mainloop()

# Ventana del dashboard interactivo
def iniciar_dashboard():
    ventana_dashboard = tk.Toplevel()
    ventana_dashboard.title("Dashboard de Cuna Inteligente")

    # Frame para organizar los gráficos horizontalmente
    frame_graficos = tk.Frame(ventana_dashboard)
    frame_graficos.pack()

    # Etiquetas para los gráficos de temperatura y humedad
    temp_img_label = tk.Label(frame_graficos)
    temp_img_label.pack(side=tk.LEFT, padx=10)  # Separación entre las gráficas

    hum_img_label = tk.Label(frame_graficos)
    hum_img_label.pack(side=tk.LEFT, padx=10)

    actualizar = True

    def on_closing():
        nonlocal actualizar
        actualizar = False
        ventana_dashboard.destroy()

    ventana_dashboard.protocol("WM_DELETE_WINDOW", on_closing)

    def actualizar_graficos():
        nonlocal actualizar
        while actualizar:
            conexion = conectar_bd()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT fecha, temperatura FROM registroTemperatura ORDER BY fecha DESC LIMIT 10")
                data_temp = cursor.fetchall()
                fechas_temp = [row[0] for row in data_temp]
                temp = [row[1] for row in data_temp]

                cursor.execute("SELECT fecha, humedad FROM registroHumedad ORDER BY fecha DESC LIMIT 10")
                data_hum = cursor.fetchall()
                fechas_hum = [row[0] for row in data_hum]
                hum = [row[1] for row in data_hum]

                conexion.close()

                # Crear gráficos de temperatura y humedad
                fig_temp = go.Figure(data=[go.Scatter(x=fechas_temp, y=temp, mode='lines+markers', name="Temperatura")])
                fig_temp.update_layout(title="Temperatura en Tiempo Real", xaxis_title="Fecha", yaxis_title="Temperatura (°C)")
                temp_image = pio.to_image(fig_temp, format="png")

                fig_hum = go.Figure(data=[go.Scatter(x=fechas_hum, y=hum, mode='lines+markers', name="Humedad")])
                fig_hum.update_layout(title="Humedad en Tiempo Real", xaxis_title="Fecha", yaxis_title="Humedad (%)")
                hum_image = pio.to_image(fig_hum, format="png")

                # Actualizar los gráficos si la ventana está abierta
                if temp_img_label.winfo_exists() and hum_img_label.winfo_exists():
                    temp_img = ImageTk.PhotoImage(Image.open(io.BytesIO(temp_image)))
                    hum_img = ImageTk.PhotoImage(Image.open(io.BytesIO(hum_image)))

                    temp_img_label.config(image=temp_img)
                    temp_img_label.image = temp_img
                    hum_img_label.config(image=hum_img)
                    hum_img_label.image = hum_img

            time.sleep(2)

    threading.Thread(target=actualizar_graficos, daemon=True).start()


if __name__ == "__main__":
    ventana_inicio()