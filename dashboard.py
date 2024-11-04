import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from datetime import datetime
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import threading
import webbrowser

# Conexión a la base de datos
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Cambia si tienes una contraseña para MySQL
        database="cunainteligente"
    )

# Consultas a la base de datos
def get_baby_data():
    conn = connect_db()
    query = "SELECT nombre, fechaDeNacimiento, peso, HoraUltimaComida FROM bebe"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_humidity_data():
    conn = connect_db()
    query = "SELECT fecha, tiempoHumedad FROM registroHumedad"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_crying_data():
    conn = connect_db()
    query = "SELECT fecha, tiempoLLanto FROM registroLLanto"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Configuración de Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Interactivo de Cuna Inteligente"),
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0),

    # Gráfico de Humedad
    dcc.Graph(id='humidity-graph'),

    # Gráfico de Llanto
    dcc.Graph(id='crying-graph')
])

# Callbacks de Dash para actualizar gráficos en tiempo real
@app.callback(
    [Output('humidity-graph', 'figure'), Output('crying-graph', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_dash_graphs(n):
    humidity_data = get_humidity_data()
    crying_data = get_crying_data()

    # Configuración del gráfico de Humedad
    fig_humidity = go.Figure(
        data=[go.Scatter(x=humidity_data['fecha'], y=humidity_data['tiempoHumedad'], mode='lines+markers')],
        layout=go.Layout(title="Tiempo de Humedad", xaxis={'title': 'Fecha'}, yaxis={'title': 'Tiempo de Humedad'})
    )

    # Configuración del gráfico de Llanto
    fig_crying = go.Figure(
        data=[go.Scatter(x=crying_data['fecha'], y=crying_data['tiempoLLanto'], mode='lines+markers')],
        layout=go.Layout(title="Tiempo de Llanto", xaxis={'title': 'Fecha'}, yaxis={'title': 'Tiempo de Llanto'})
    )

    return fig_humidity, fig_crying

# Hilo para ejecutar Dash
def run_dash():
    app.run_server(debug=True, use_reloader=False)

# Configuración de gráficos en Tkinter usando Matplotlib
def update_tkinter_charts():
    baby_data = get_baby_data()
    fig_weight.clear()
    fig_last_meal.clear()

    # Opción 1: Contador de Tiempo Transcurrido desde la Última Comida
    text_widget.delete("1.0", tk.END)
    for _, row in baby_data.iterrows():
        name = row['nombre']
        last_meal_time = pd.to_datetime(row['HoraUltimaComida'])
        time_since_last_meal = datetime.now() - last_meal_time
        hours, remainder = divmod(time_since_last_meal.total_seconds(), 3600)
        minutes = remainder // 60
        text_widget.insert(tk.END, f"{name}: {int(hours)} horas, {int(minutes)} minutos\n")

    # Opción 2: Gráfico de Barras Horizontales para el Tiempo Transcurrido desde la Última Comida
    ax1 = fig_last_meal.add_subplot(111)
    times = [(datetime.now() - pd.to_datetime(row['HoraUltimaComida'])).total_seconds() / 3600 for _, row in baby_data.iterrows()]
    names = baby_data['nombre']
    ax1.barh(names, times, color='lightblue')
    ax1.set_title("Horas desde la última comida")
    ax1.set_xlabel("Horas")
    canvas_last_meal.draw()

    # Gráfico de comparación de peso
    ax2 = fig_weight.add_subplot(111)
    ages = [(datetime.now() - pd.to_datetime(row['fechaDeNacimiento'])).days / 30.44 for _, row in baby_data.iterrows()]
    actual_weights = baby_data['peso']
    expected_weights = [3 + 0.7 * age for age in ages]  # Peso estimado
    ax2.plot(ages, actual_weights, 'o-', label='Peso Real')
    ax2.plot(ages, expected_weights, 'x--', label='Peso Esperado')
    ax2.set_title("Comparación de Peso")
    ax2.set_xlabel("Edad (meses)")
    ax2.set_ylabel("Peso (kg)")
    ax2.legend()
    canvas_weight.draw()

    # Refrescar cada 5 segundos
    root.after(5000, update_tkinter_charts)

# Configuración de la interfaz Tkinter
root = tk.Tk()
root.title("Dashboard de Cuna Inteligente")

# Botón para abrir el Dashboard de Dash en el navegador
def open_dashboard():
    webbrowser.open("http://127.0.0.1:8050")

tk.Button(root, text="Abrir Dashboard Interactivo", command=open_dashboard).pack()

# Opción 1: Contador de Tiempo Transcurrido en Tkinter
text_widget = tk.Text(root, height=10, width=40)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Gráfico en Tkinter de tiempo desde la última comida (Opción 2)
fig_last_meal = plt.Figure(figsize=(5, 4), dpi=100)
canvas_last_meal = FigureCanvasTkAgg(fig_last_meal, master=root)
canvas_last_meal.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Gráfico en Tkinter de comparación de peso
fig_weight = plt.Figure(figsize=(5, 4), dpi=100)
canvas_weight = FigureCanvasTkAgg(fig_weight, master=root)
canvas_weight.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Iniciar el dashboard de Dash en un hilo separado
threading.Thread(target=run_dash).start()

# Iniciar la actualización de los gráficos en Tkinter
update_tkinter_charts()
root.mainloop()