import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
import matplotlib.pyplot as plt
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

# Función para obtener datos de la base de datos
def obtener_datos(query):
    conexion = conectar_bd()
    if conexion:
        cursor = conexion.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()
        conexion.close()
        return datos
    return []

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
    ventana_registro.geometry("400x400")
    ventana_registro.configure(bg="#f0f0f0")

    header = ttk.Label(ventana_registro, text="Registro de Usuario", font=("Arial", 16, "bold"), background="#f0f0f0")
    header.pack(pady=(10, 20))

    form_frame = ttk.Frame(ventana_registro, padding=20)
    form_frame.pack(fill='both', expand=True)

    ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
    entry_nombre = ttk.Entry(form_frame, width=30)
    entry_nombre.grid(row=0, column=1, pady=5)

    ttk.Label(form_frame, text="Apellido Paterno:").grid(row=1, column=0, sticky="w", pady=5)
    entry_apellido_p = ttk.Entry(form_frame, width=30)
    entry_apellido_p.grid(row=1, column=1, pady=5)

    ttk.Label(form_frame, text="Apellido Materno:").grid(row=2, column=0, sticky="w", pady=5)
    entry_apellido_m = ttk.Entry(form_frame, width=30)
    entry_apellido_m.grid(row=2, column=1, pady=5)

    ttk.Label(form_frame, text="Usuario:").grid(row=3, column=0, sticky="w", pady=5)
    entry_username = ttk.Entry(form_frame, width=30)
    entry_username.grid(row=3, column=1, pady=5)

    ttk.Label(form_frame, text="Correo Gmail:").grid(row=4, column=0, sticky="w", pady=5)
    entry_gmail = ttk.Entry(form_frame, width=30)
    entry_gmail.grid(row=4, column=1, pady=5)

    ttk.Label(form_frame, text="Contraseña:").grid(row=5, column=0, sticky="w", pady=5)
    entry_password = ttk.Entry(form_frame, show="*", width=30)
    entry_password.grid(row=5, column=1, pady=5)

    ttk.Button(ventana_registro, text="Registrar", command=registrar).pack(pady=20)

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
    ventana.geometry("400x300")
    ventana.configure(bg="#f0f0f0")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=10)
    style.configure("TEntry", font=("Arial", 12))
    
    header = ttk.Label(ventana, text="Bienvenido", font=("Arial", 18, "bold"), background="#f0f0f0")
    header.pack(pady=(20, 10))

    user_frame = ttk.Frame(ventana)
    user_frame.pack(pady=(5, 10))
    ttk.Label(user_frame, text="Usuario:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=5)
    entry_user = ttk.Entry(user_frame, width=25)
    entry_user.grid(row=0, column=1)

    pass_frame = ttk.Frame(ventana)
    pass_frame.pack(pady=(5, 10))
    ttk.Label(pass_frame, text="Contraseña:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=5)
    entry_pass = ttk.Entry(pass_frame, show="*", width=25)
    entry_pass.grid(row=0, column=1)

    btn_frame = ttk.Frame(ventana)
    btn_frame.pack(pady=20)
    ttk.Button(btn_frame, text="Ingresar", command=login).grid(row=0, column=0, padx=5)
    ttk.Button(btn_frame, text="Registrarse", command=ventana_registro).grid(row=0, column=1, padx=5)

    ventana.mainloop()

# Ventana para selección de bebés
def seleccionar_bebe():
    def cargar_bebes():
        for widget in frame_bebes.winfo_children():
            widget.destroy()

        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT id_bebe, nombre, apellidoPaterno FROM bebe WHERE usuario_id_usuario=%s", (id_usuario,))
            bebes = cursor.fetchall()
            conexion.close()
            
            for bebe in bebes:
                id_bebe, nombre, apellidoPaterno = bebe
                boton_bebe = ttk.Button(frame_bebes, text=f"{nombre} {apellidoPaterno}", command=iniciar_dashboard)
                boton_bebe.pack(fill='x', pady=5)

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
                cargar_bebes()

        ventana_agregar_bebe = tk.Toplevel(ventana_bebe)
        ventana_agregar_bebe.title("Registrar Nuevo Bebé")
        ventana_agregar_bebe.geometry("350x250")
        ventana_agregar_bebe.configure(bg="#f0f0f0")

        header = ttk.Label(ventana_agregar_bebe, text="Registrar Nuevo Bebé", font=("Arial", 14, "bold"), background="#f0f0f0")
        header.pack(pady=(10, 10))

        form_frame = ttk.Frame(ventana_agregar_bebe, padding=10)
        form_frame.pack(fill='both', expand=True)

        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        entry_nombre = ttk.Entry(form_frame, width=25)
        entry_nombre.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Apellido Paterno:").grid(row=1, column=0, sticky="w", pady=5)
        entry_apellido_p = ttk.Entry(form_frame, width=25)
        entry_apellido_p.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Apellido Materno:").grid(row=2, column=0, sticky="w", pady=5)
        entry_apellido_m = ttk.Entry(form_frame, width=25)
        entry_apellido_m.grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Fecha de Nacimiento (AAAA-MM-DD):").grid(row=3, column=0, sticky="w", pady=5)
        entry_fecha_nac = ttk.Entry(form_frame, width=25)
        entry_fecha_nac.grid(row=3, column=1, pady=5)

        ttk.Button(ventana_agregar_bebe, text="Registrar", command=registrar_nuevo_bebe).pack(pady=10)

    ventana_bebe = tk.Tk()
    ventana_bebe.title("Seleccionar Bebé")
    ventana_bebe.geometry("400x300")
    ventana_bebe.configure(bg="#f0f0f0")

    header = ttk.Label(ventana_bebe, text="Selecciona un Bebé", font=("Arial", 16, "bold"), background="#f0f0f0")
    header.pack(pady=(20, 10))

    frame_bebes = ttk.Frame(ventana_bebe, padding=10)
    frame_bebes.pack(fill='both', expand=True)

    cargar_bebes()

    ttk.Button(ventana_bebe, text="Añadir Bebé", command=agregar_bebe).pack(pady=10)

    ventana_bebe.mainloop()

# Ventana del dashboard interactivo
def iniciar_dashboard():
    ventana_dashboard = tk.Toplevel()
    ventana_dashboard.title("Dashboard de Cuna Inteligente")
    ventana_dashboard.geometry("800x600")

    # Crear marcos para los gráficos
    frame_graficos = tk.Frame(ventana_dashboard)
    frame_graficos.pack(pady=20)

    temp_img_label = tk.Label(frame_graficos)
    temp_img_label.grid(row=0, column=0, padx=20)

    hum_img_label = tk.Label(frame_graficos)
    hum_img_label.grid(row=0, column=1, padx=20)

    actualizar = True

    def on_closing():
        nonlocal actualizar
        actualizar = False
        ventana_dashboard.destroy()

    ventana_dashboard.protocol("WM_DELETE_WINDOW", on_closing)

    def actualizar_graficos():
        nonlocal actualizar
        while actualizar:
            temperaturas = obtener_datos("SELECT fecha, temperatura FROM registroTemperatura ORDER BY fecha DESC LIMIT 10")
            humedades = obtener_datos("SELECT fecha, humedad FROM registroHumedad ORDER BY fecha DESC LIMIT 10")

            if temperaturas:
                fechas, temp_vals = zip(*temperaturas)
                plt.figure(figsize=(4, 3))
                plt.plot(fechas, temp_vals, color='red', marker='o')
                plt.title("Temperatura (Últimos 10 registros)")
                plt.xlabel("Fecha")
                plt.ylabel("Temperatura (°C)")
                plt.grid(True)
                temp_buf = io.BytesIO()
                plt.savefig(temp_buf, format="png")
                temp_buf.seek(0)
                temp_img = Image.open(temp_buf)
                temp_img = ImageTk.PhotoImage(temp_img)
                temp_img_label.configure(image=temp_img)
                temp_img_label.image = temp_img
                plt.close()

            if humedades:
                fechas, hum_vals = zip(*humedades)
                plt.figure(figsize=(4, 3))
                plt.plot(fechas, hum_vals, color='blue', marker='o')
                plt.title("Humedad (Últimos 10 registros)")
                plt.xlabel("Fecha")
                plt.ylabel("Humedad (%)")
                plt.grid(True)
                hum_buf = io.BytesIO()
                plt.savefig(hum_buf, format="png")
                hum_buf.seek(0)
                hum_img = Image.open(hum_buf)
                hum_img = ImageTk.PhotoImage(hum_img)
                hum_img_label.configure(image=hum_img)
                hum_img_label.image = hum_img
                plt.close()

            time.sleep(5)

    threading.Thread(target=actualizar_graficos, daemon=True).start()

# Iniciar la aplicación
ventana_inicio()