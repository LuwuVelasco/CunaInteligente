import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import mysql.connector
import matplotlib.pyplot as plt
import threading
import time
import io
from queue import Queue
import queue

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
def obtener_datos(query, params=()):
    try:
        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute(query, params)
            datos = cursor.fetchall()
            conexion.close()
            return datos
    except mysql.connector.Error as err:
        print(f"Error al obtener datos: {err}")
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
    ventana_registro.geometry("400x360")
    ventana_registro.configure(bg="#f0f0f0")

    # Centrar ventana
    ancho_ventana = 400
    alto_ventana = 360
    ancho_pantalla = ventana_registro.winfo_screenwidth()
    alto_pantalla = ventana_registro.winfo_screenheight()
    x_ventana = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y_ventana = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana_registro.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")
    
    # Cargar imagen de fondo
    imagen_fondo = Image.open("FONDO_DASH.jpg")  # Reemplaza con la ruta de tu imagen
    imagen_fondo = imagen_fondo.resize((400, 360), Image.LANCZOS)  # Ajusta el tamaño de la imagen
    fondo = ImageTk.PhotoImage(imagen_fondo)
    
    label_fondo = tk.Label(ventana_registro, image=fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.image = fondo  # Referencia para evitar que se elimine la imagen

    # Contenedor central
    frame_central = ttk.Frame(ventana_registro, padding=20)
    frame_central.pack(expand=True)

    header = ttk.Label(frame_central, text="Registro de Usuario", font=("Arial", 16, "bold"), background="")
    header.grid(row=0, column=0, columnspan=2, pady=(10, 20))

    ttk.Label(frame_central, text="Nombre:").grid(row=1, column=0, sticky="e", pady=5)
    entry_nombre = ttk.Entry(frame_central, width=30)
    entry_nombre.grid(row=1, column=1, pady=5)

    ttk.Label(frame_central, text="Apellido Paterno:").grid(row=2, column=0, sticky="e", pady=5)
    entry_apellido_p = ttk.Entry(frame_central, width=30)
    entry_apellido_p.grid(row=2, column=1, pady=5)

    ttk.Label(frame_central, text="Apellido Materno:").grid(row=3, column=0, sticky="e", pady=5)
    entry_apellido_m = ttk.Entry(frame_central, width=30)
    entry_apellido_m.grid(row=3, column=1, pady=5)

    ttk.Label(frame_central, text="Usuario:").grid(row=4, column=0, sticky="e", pady=5)
    entry_username = ttk.Entry(frame_central, width=30)
    entry_username.grid(row=4, column=1, pady=5)

    ttk.Label(frame_central, text="Correo Gmail:").grid(row=5, column=0, sticky="e", pady=5)
    entry_gmail = ttk.Entry(frame_central, width=30)
    entry_gmail.grid(row=5, column=1, pady=5)

    ttk.Label(frame_central, text="Contraseña:").grid(row=6, column=0, sticky="e", pady=5)
    entry_password = ttk.Entry(frame_central, show="*", width=30)
    entry_password.grid(row=6, column=1, pady=5)

    ttk.Button(frame_central, text="Registrar", command=registrar).grid(row=7, column=0, columnspan=2, pady=20)

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
    ventana.geometry("400x360")
    ventana.configure(bg="#f0f0f0")

    # Centrar ventana en la pantalla
    ancho_ventana = 400
    alto_ventana = 360
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    x_ventana = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y_ventana = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")
    
    # Cargar imagen de fondo
    imagen_fondo = Image.open("FONDO_DASH.jpg")  # Reemplaza con la ruta de tu imagen
    imagen_fondo = imagen_fondo.resize((400, 360), Image.LANCZOS)  # Ajusta el tamaño de la imagen
    fondo = ImageTk.PhotoImage(imagen_fondo)
    
    label_fondo = tk.Label(ventana, image=fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

    # Crear un marco para centrar los elementos
    container = tk.Frame(ventana, bg="#f0f0f0")
    container.pack(expand=True)  # Expandir y centrar el marco

    # Añadir los componentes en el marco container
    header = ttk.Label(container, text="Bienvenido", font=("Arial", 18, "bold"), background="#f0f0f0")
    header.pack(pady=(20, 10))

    user_frame = ttk.Frame(container)
    user_frame.pack(pady=(5, 10))
    ttk.Label(user_frame, text="Usuario:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=5)
    entry_user = ttk.Entry(user_frame, width=25)
    entry_user.grid(row=0, column=1)

    pass_frame = ttk.Frame(container)
    pass_frame.pack(pady=(5, 10))
    ttk.Label(pass_frame, text="Contraseña:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=5)
    entry_pass = ttk.Entry(pass_frame, show="*", width=25)
    entry_pass.grid(row=0, column=1)

    btn_frame = ttk.Frame(container)
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

    # Ventana para agregar un bebé
    def agregar_bebe():
        def guardar_bebe():
            nombre = entry_nombre.get()
            apellido = entry_apellido.get()
            fecha_nacimiento = entry_fecha_nacimiento.get()

            if nombre and apellido and fecha_nacimiento:
                conexion = conectar_bd()
                if conexion:
                    cursor = conexion.cursor()
                    cursor.execute("INSERT INTO bebe (nombre, apellido, fecha_nacimiento) VALUES (%s, %s, %s)",
                                   (nombre, apellido, fecha_nacimiento))
                    conexion.commit()
                    conexion.close()
                    messagebox.showinfo("Éxito", "Bebé agregado exitosamente")
                    ventana_agregar_bebe.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo agregar al bebé")
            else:
                messagebox.showwarning("Advertencia", "Por favor, completa todos los campos")

        ventana_agregar_bebe = tk.Toplevel()
        ventana_agregar_bebe.title("Agregar Bebé")
        ventana_agregar_bebe.geometry("400x360")
        ventana_agregar_bebe.configure(bg="#f0f0f0")

        # Centrar ventana
        ancho_ventana = 400
        alto_ventana = 360
        ancho_pantalla = ventana_agregar_bebe.winfo_screenwidth()
        alto_pantalla = ventana_agregar_bebe.winfo_screenheight()
        x_ventana = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y_ventana = (alto_pantalla // 2) - (alto_ventana // 2)
        ventana_agregar_bebe.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")
        
        # Cargar imagen de fondo
        imagen_fondo = Image.open("FONDO_DASH.jpg")  # Reemplaza con la ruta de tu imagen
        imagen_fondo = imagen_fondo.resize((400, 360), Image.LANCZOS)  # Ajusta el tamaño de la imagen
        fondo = ImageTk.PhotoImage(imagen_fondo)
        
        label_fondo = tk.Label(ventana_agregar_bebe, image=fondo)
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        label_fondo.image = fondo
        
        # Contenedor central
        frame_central = ttk.Frame(ventana_agregar_bebe, padding=20)
        frame_central.pack(expand=True)

        header = ttk.Label(frame_central, text="Agregar Bebé", font=("Arial", 16, "bold"), background="#f0f0f0")
        header.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        ttk.Label(frame_central, text="Nombre:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
        entry_nombre = ttk.Entry(frame_central, width=25)
        entry_nombre.grid(row=1, column=1, pady=5)

        ttk.Label(frame_central, text="Apellido:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
        entry_apellido = ttk.Entry(frame_central, width=25)
        entry_apellido.grid(row=2, column=1, pady=5)

        ttk.Label(frame_central, text="Nacimiento\n(AAAA-MM-DD):", font=("Arial", 12)).grid(row=3, column=0, sticky="e", pady=5)
        entry_fecha_nacimiento = ttk.Entry(frame_central, width=25)
        entry_fecha_nacimiento.grid(row=3, column=1, pady=5)

        ttk.Button(frame_central, text="Guardar", command=guardar_bebe).grid(row=4, column=0, columnspan=2, pady=20)

    ventana_bebe = tk.Toplevel()
    ventana_bebe.title("Seleccionar Bebé")
    ventana_bebe.geometry("400x360")
    ventana_bebe.configure(bg="#f0f0f0")

    # Centrar ventana
    ancho_ventana = 400
    alto_ventana = 360
    ancho_pantalla = ventana_bebe.winfo_screenwidth()
    alto_pantalla = ventana_bebe.winfo_screenheight()
    x_ventana = (ancho_pantalla // 2) - (ancho_ventana // 2)
    y_ventana = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana_bebe.geometry(f"{ancho_ventana}x{alto_ventana}+{x_ventana}+{y_ventana}")
    
    # Cargar imagen de fondo en ventana de seleccionar bebé
    imagen_fondo = Image.open("FONDO_DASH.jpg")
    imagen_fondo = imagen_fondo.resize((400, 360), Image.LANCZOS)
    fondo = ImageTk.PhotoImage(imagen_fondo)
    
    label_fondo = tk.Label(ventana_bebe, image=fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.image = fondo

    header = ttk.Label(ventana_bebe, text="Seleccionar Bebé", font=("Arial", 16, "bold"), background="#f0f0f0")
    header.pack(pady=10)

    frame_bebes = ttk.Frame(ventana_bebe, padding=10)
    frame_bebes.pack(fill='both', expand=True)

    cargar_bebes()

    ttk.Button(ventana_bebe, text="Agregar Bebé", command=agregar_bebe).pack(pady=10)
    ventana_bebe.mainloop()

# Ventana del dashboard interactivo
def iniciar_dashboard():
    ventana_dashboard = tk.Toplevel()
    ventana_dashboard.title("Dashboard de Cuna Inteligente")
    ventana_dashboard.state("zoomed")  # Maximizar la ventana

    # Contenedor principal con canvas para permitir scroll
    canvas = tk.Canvas(ventana_dashboard)
    canvas.pack(side="left", fill="both", expand=True)
    
    # Cargar imagen de fondo en el dashboard
    imagen_fondo = Image.open("FONDO_DASH.jpg")
    imagen_fondo = imagen_fondo.resize((1500, 800), Image.LANCZOS)
    fondo = ImageTk.PhotoImage(imagen_fondo)
    
    label_fondo = tk.Label(canvas, image=fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
    label_fondo.image = fondo

    # Scrollbar para el canvas
    scrollbar = ttk.Scrollbar(ventana_dashboard, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Crear un frame dentro del canvas
    dashboard_frame = ttk.Frame(canvas)
    dashboard_frame.pack(anchor="center")
    canvas.create_window((250, 0), window=dashboard_frame, anchor="nw")

    # Configurar el frame para actualizar el tamaño del canvas
    def ajustar_canvas(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    dashboard_frame.bind("<Configure>", ajustar_canvas)

    # Crear tarjetas para los contadores e indicadores
    frame_tarjetas = ttk.Frame(dashboard_frame)
    frame_tarjetas.pack(pady=10, anchor="center")

    # Tarjeta de Temperatura
    temp_frame = tk.Frame(frame_tarjetas, bg="white", bd=2, relief="groove", padx=10, pady=5)
    temp_frame.grid(row=0, column=0, padx=10, pady=10)
    temp_val_label = tk.Label(temp_frame, text="Temperatura Actual: N/A", font=("Arial", 12, "bold"), bg="white")
    temp_val_label.pack()
    temp_status_label = tk.Label(temp_frame, text="Condición de Temperatura: N/A", font=("Arial", 10), bg="white")
    temp_status_label.pack()

    # Tarjeta de Humedad
    hum_frame = tk.Frame(frame_tarjetas, bg="white", bd=2, relief="groove", padx=10, pady=5)
    hum_frame.grid(row=0, column=1, padx=10, pady=10)
    hum_val_label = tk.Label(hum_frame, text="Humedad Actual: N/A", font=("Arial", 12, "bold"), bg="white")
    hum_val_label.pack()
    hum_status_label = tk.Label(hum_frame, text="Condición de Humedad: N/A", font=("Arial", 10), bg="white")
    hum_status_label.pack()
    
    # Función para actualizar el color del estado
    def actualizar_estado_label(framel, label, main_label, texto, seguro):
        label.config(text=texto)
        if seguro:
            framel.config(background="#00bb2d")
            label.config(background="#00bb2d", foreground="white")  # Verde para seguro
            main_label.config(background="#00bb2d", foreground="white")
        else:
            framel.config(background="#b81414")
            label.config(background="#b81414", foreground="white")  # Rojo para inseguro
            main_label.config(background="#b81414", foreground="white")

    # Entrada para definir el número de registros
    filtro_frame = ttk.Frame(dashboard_frame)
    filtro_frame.pack(pady=10, anchor="center")
    ttk.Label(filtro_frame, text="Número de registros recientes:").grid(row=0, column=0, padx=5)
    entry_limite = ttk.Entry(filtro_frame, width=5)
    entry_limite.grid(row=0, column=1, padx=5)
    entry_limite.insert(0, "10")

    # Contenido del dashboard
    frame_graficos = tk.Frame(dashboard_frame)
    frame_graficos.pack(pady=20, anchor="center")

    temp_img_label = tk.Label(frame_graficos)
    temp_img_label.grid(row=0, column=0, padx=20)

    hum_img_label = tk.Label(frame_graficos)
    hum_img_label.grid(row=0, column=1, padx=20)
    
    # Frame para tablas
    frame_tablas = tk.Frame(dashboard_frame)
    frame_tablas.pack(pady=10, anchor="center")
    
    # Tabla de datos de temperatura (posición izquierda)
    temp_table = ttk.Treeview(frame_tablas, columns=("Fecha", "Temperatura"), show="headings")
    temp_table.heading("Fecha", text="Fecha")
    temp_table.heading("Temperatura", text="Temperatura (°C)")
    temp_table.grid(row=0, column=0, padx=10)  # Usa grid y coloca en la columna 0

    # Tabla de datos de humedad (posición derecha)
    hum_table = ttk.Treeview(frame_tablas, columns=("Fecha", "Humedad"), show="headings")
    hum_table.heading("Fecha", text="Fecha")
    hum_table.heading("Humedad", text="Humedad (%)")
    hum_table.grid(row=0, column=1, padx=10)  # Coloca en la columna 1, misma fila

    # Cola para manejar los datos de actualización desde el hilo secundario
    update_queue = Queue()

    actualizar = True

    def on_closing():
        nonlocal actualizar
        actualizar = False
        ventana_dashboard.destroy()

    ventana_dashboard.protocol("WM_DELETE_WINDOW", on_closing)

    # Función para obtener el número de registros en una tabla
    def contar_registros(tabla):
        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            conexion.close()
            return count
        return 0

    # Función de actualización de gráficos y tablas con verificación de límite
    def obtener_datos_graficos():
        while actualizar:
            try:
                limite = int(entry_limite.get())  # Leer el valor del límite de registros
                
                # Verificar el número de registros disponibles en cada tabla
                total_temp = contar_registros("registroTemperatura")
                total_hum = contar_registros("registroHumedad")
                
                # Comprobar si el límite excede el total de registros disponibles
                if limite > total_temp or limite > total_hum:
                    messagebox.showwarning("Advertencia", "Solicitó más datos de los que hay en temperatura o humedad. Volviendo al límite de 10.")
                    limite = 10
                    entry_limite.delete(0, tk.END)
                    entry_limite.insert(0, "10")
                
                # Obtener los datos con el límite ajustado
                temperaturas = obtener_datos(f"SELECT fecha, temperatura FROM registroTemperatura ORDER BY fecha DESC LIMIT {limite}")
                humedades = obtener_datos(f"SELECT fecha, humedad FROM registroHumedad ORDER BY fecha DESC LIMIT {limite}")

                if temperaturas and humedades:
                    fechas_temp, temp_vals = zip(*temperaturas)
                    fechas_hum, hum_vals = zip(*humedades)

                    update_queue.put((fechas_temp, temp_vals, fechas_hum, hum_vals, temperaturas, humedades))

                time.sleep(5)

            except ValueError:
                messagebox.showerror("Error", "El número de registros debe ser un valor numérico.")
                entry_limite.delete(0, tk.END)
                entry_limite.insert(0, "10")

    # Función de actualización en el hilo principal
    def actualizar_dashboard():
        try:
            fechas_temp, temp_vals, fechas_hum, hum_vals, temperaturas, humedades = update_queue.get_nowait()

            # Actualizar contadores
            temp_val_label.config(text=f"Temperatura Actual: {temp_vals[0]} °C")
            hum_val_label.config(text=f"Humedad Actual: {hum_vals[0]} %")

            # Indicadores de condiciones seguras
            actualizar_estado_label(temp_frame, temp_status_label, temp_val_label, "Condición de Temperatura: Segura" if 20 <= temp_vals[0] <= 30 else "Condición de Temperatura: Insegura", 20 <= temp_vals[0] <= 30)
            actualizar_estado_label(hum_frame, hum_status_label, hum_val_label, "Condición de Humedad: Segura" if 40 <= hum_vals[0] <= 60 else "Condición de Humedad: Insegura", 40 <= hum_vals[0] <= 60)

            # Actualizar tabla de temperatura
            temp_table.delete(*temp_table.get_children())
            for fecha, temp in temperaturas:
                temp_table.insert("", "end", values=(fecha, temp))

            # Actualizar tabla de humedad
            hum_table.delete(*hum_table.get_children())
            for fecha, hum in humedades:
                hum_table.insert("", "end", values=(fecha, hum))

            # Gráfico de temperatura
            plt.figure(figsize=(4, 4))
            plt.plot(fechas_temp, temp_vals, color='red', marker='o')
            plt.title("Registros Temperatura")
            plt.xlabel("Fecha")
            plt.xticks(rotation=90)
            plt.ylabel("Temperatura (°C)")
            plt.grid(True)
            plt.tight_layout()  # Ajusta el layout para evitar recortes
            plt.gcf().autofmt_xdate()  # Ajuste automático de fechas
            temp_buf = io.BytesIO()
            plt.savefig(temp_buf, format="png")
            temp_buf.seek(0)
            temp_img = Image.open(temp_buf)
            temp_img = ImageTk.PhotoImage(temp_img)
            temp_img_label.configure(image=temp_img)
            temp_img_label.image = temp_img
            plt.close()

            # Gráfico de humedad
            plt.figure(figsize=(4, 4))
            plt.plot(fechas_hum, hum_vals, color='blue', marker='o')
            plt.title("Registros Humedad")
            plt.xlabel("Fecha")
            plt.xticks(rotation=90)
            plt.ylabel("Humedad (%)")
            plt.grid(True)
            plt.tight_layout()
            plt.gcf().autofmt_xdate()
            hum_buf = io.BytesIO()
            plt.savefig(hum_buf, format="png")
            hum_buf.seek(0)
            hum_img = Image.open(hum_buf)
            hum_img = ImageTk.PhotoImage(hum_img)
            hum_img_label.configure(image=hum_img)
            hum_img_label.image = hum_img
            plt.close()

        except queue.Empty:
            pass

        ventana_dashboard.after(100, actualizar_dashboard)

    threading.Thread(target=obtener_datos_graficos, daemon=True).start()
    actualizar_dashboard()

# Iniciar la aplicación
ventana_inicio()