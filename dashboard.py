import mysql.connector
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import threading

# Conexión a la base de datos
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Cambia si tienes una contraseña para MySQL
        database="cunainteligente"
    )

# Función de inicio de sesión
def login(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario WHERE usuario=%s AND contrasenia=%s", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result

# Función de registro de usuario
def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuario (usuario, contrasenia) VALUES (%s, %s)", (username, password))
        conn.commit()
        messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al registrar usuario: {err}")
    conn.close()

# Función para seleccionar bebé
def get_babies_for_user():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id_bebe, nombre FROM bebe")
    data = cursor.fetchall()
    conn.close()
    return data

# Función para registrar un bebé
def register_baby(name, birth_date):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO bebe (nombre, fechaDeNacimiento) VALUES (%s, %s)", (name, birth_date))
        conn.commit()
        messagebox.showinfo("Registro exitoso", f"Bebé {name} registrado correctamente")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al registrar bebé: {err}")
    conn.close()

# Función para iniciar el dashboard de Dash
def start_dash_server():
    app = Dash(__name__)

    app.layout = html.Div([
        html.H1("Gráfica en Tiempo Real"),
        dcc.Graph(id='live-graph'),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
    ])

    @app.callback(Output('live-graph', 'figure'), [Input('interval-component', 'n_intervals')])
    def update_graph(n):
        engine = connect_db()
        query = "SELECT timestamp, metric FROM registroCaracteristicas ORDER BY timestamp DESC LIMIT 10"
        data = pd.read_sql(query, engine)

        # Configuración del gráfico de Dash
        fig = {
            'data': [{'x': data['timestamp'], 'y': data['metric'], 'type': 'line', 'name': 'Metric'}],
            'layout': {'title': 'Metric en Tiempo Real'}
        }
        return fig

    app.run_server(debug=False)

# Función para mostrar el dashboard de Tkinter
def show_dashboard(baby_id):
    dashboard_window = tk.Toplevel()
    dashboard_window.title("Dashboard del Bebé")

    # Obtener datos del bebé
    engine = connect_db()
    query = f"SELECT * FROM registroCaracteristicas WHERE bebe_id_bebe={baby_id}"
    baby_data = pd.read_sql(query, engine)

    # Verificar que las columnas existen antes de graficar
    if 'timestamp' not in baby_data.columns or 'metric' not in baby_data.columns:
        messagebox.showerror("Error", "La columna 'timestamp' o 'metric' no existe en los datos.")
        dashboard_window.destroy()
        return

    # Crear gráficos usando matplotlib
    fig, ax = plt.subplots()
    ax.plot(baby_data['timestamp'], baby_data['metric'], label="Métrica")
    ax.set_title("Gráfica de Métrica del Bebé")
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Métrica")
    ax.legend()

    # Mostrar gráfico en el panel
    canvas = FigureCanvasTkAgg(fig, master=dashboard_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Tabla de datos
    table_frame = tk.Frame(dashboard_window)
    table_frame.pack()
    for i, col in enumerate(baby_data.columns):
        tk.Label(table_frame, text=col).grid(row=0, column=i)
    for row, record in enumerate(baby_data.itertuples(), start=1):
        for col, value in enumerate(record[1:]):
            tk.Label(table_frame, text=value).grid(row=row, column=col)

    # Botón para abrir Dash
    def open_dash():
        threading.Thread(target=start_dash_server).start()

    tk.Button(dashboard_window, text="Ver Gráfica en Tiempo Real", command=open_dash).pack()

# Interfaz de usuario con tkinter
def main():
    def handle_login():
        username = entry_username.get()
        password = entry_password.get()
        if login(username, password):
            messagebox.showinfo("Inicio de sesión exitoso", f"Bienvenido, {username}")
            window.destroy()
            select_baby()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def handle_register():
        username = entry_username.get()
        password = entry_password.get()
        register_user(username, password)

    def select_baby():
        baby_window = tk.Tk()
        baby_window.title("Selecciona o Registra un Bebé")

        # Campo para ingresar el nombre del bebé
        tk.Label(baby_window, text="Nombre del Bebé").pack()
        entry_baby_name = tk.Entry(baby_window)
        entry_baby_name.pack()

        # Campo para ingresar la fecha de nacimiento del bebé
        tk.Label(baby_window, text="Fecha de Nacimiento (YYYY-MM-DD)").pack()
        entry_birth_date = tk.Entry(baby_window)
        entry_birth_date.pack()

        # Función para manejar el registro del bebé
        def handle_register_baby():
            baby_name = entry_baby_name.get()
            birth_date = entry_birth_date.get()
            if baby_name and birth_date:
                try:
                    datetime.strptime(birth_date, "%Y-%m-%d")  # Validar formato de fecha
                    register_baby(baby_name, birth_date)
                    update_baby_list()
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha incorrecto. Use YYYY-MM-DD.")
            else:
                messagebox.showerror("Error", "Complete todos los campos")

        # Botón para registrar bebé
        tk.Button(baby_window, text="Registrar Bebé", command=handle_register_baby).pack()

        # Mostrar lista de bebés existentes
        baby_list_frame = tk.Frame(baby_window)
        baby_list_frame.pack(pady=10)

        def update_baby_list():
            # Limpiar la lista actual de bebés
            for widget in baby_list_frame.winfo_children():
                widget.destroy()
            babies = get_babies_for_user()
            tk.Label(baby_list_frame, text="Seleccione un Bebé:").pack()
            for baby in babies:
                tk.Button(baby_list_frame, text=f"{baby[1]}", command=lambda b=baby[0]: show_dashboard(b)).pack()

        update_baby_list()

        baby_window.mainloop()

    # Ventana de inicio de sesión
    window = tk.Tk()
    window.title("Inicio de sesión o Registro")

    tk.Label(window, text="Usuario").pack()
    entry_username = tk.Entry(window)
    entry_username.pack()

    tk.Label(window, text="Contraseña").pack()
    entry_password = tk.Entry(window, show="*")
    entry_password.pack()

    tk.Button(window, text="Iniciar sesión", command=handle_login).pack()
    tk.Button(window, text="Registrarse", command=handle_register).pack()

    window.mainloop()

if __name__ == "__main__":
    main()