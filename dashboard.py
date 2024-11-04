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
    query = "SELECT id_bebe, nombre, fechaDeNacimiento, pesoInicial FROM bebe"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_characteristics_data():
    conn = connect_db()
    query = "SELECT fecha, peso, altura, bebe_id_bebe FROM registroCaracteristicas"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Función para obtener el peso de referencia de acuerdo con la edad
def get_reference_weight(age, is_boy=True):
    if is_boy:
        weight_reference = {0: (2.9, 3.3), 1: (3.7, 4.2), 2: (4.3, 5.0), 3: (5.0, 5.7),
                            4: (6.3, 6.3), 5: (6.9, 6.9), 6: (7.5, 7.5), 7: (8.0, 8.0),
                            9: (8.9, 8.9), 10: (9.3, 9.3), 11: (9.6, 9.6), 12: (10.0, 10.0)}
    else:
        weight_reference = {0: (2.5, 3.2), 1: (3.2, 4.0), 2: (4.0, 4.7), 3: (4.7, 5.5),
                            4: (6.1, 6.1), 5: (6.7, 6.7), 6: (7.3, 7.3), 7: (7.8, 7.8),
                            8: (8.2, 8.2), 9: (8.6, 8.6), 10: (9.1, 9.1), 11: (9.5, 9.5), 12: (9.8, 9.8)}
    return weight_reference.get(age, (0, 0))

# Función para obtener la altura de referencia de acuerdo con la edad
def get_reference_height(age, is_boy=True):
    if is_boy:
        height_reference = {0: 50, 1: 55, 2: 57, 3: 61, 4: 62, 5: 63, 
                            6: 64, 7: 66, 9: 69, 10: 71, 11: 73, 12: 75}
    else:
        height_reference = {0: 48, 1: 52, 2: 56, 3: 59, 4: 61, 5: 62, 
                            6: 63, 7: 65, 8: 67, 9: 68, 10: 70, 11: 72, 12: 73}
    return height_reference.get(age, 0)

# Configuración de Dash
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Interactivo de Cuna Inteligente"),
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0),

    # Gráfico de Peso
    dcc.Graph(id='weight-graph'),
    # Gráfico de Altura
    dcc.Graph(id='height-graph'),
])

# Callbacks de Dash para actualizar gráficos en tiempo real
@app.callback(
    [Output('weight-graph', 'figure'), Output('height-graph', 'figure')],
    Input('interval-component', 'n_intervals')
)
def update_dash_graph(n):
    baby_data = get_baby_data()
    characteristics_data = get_characteristics_data()

    # Calcular la edad en meses
    baby_data['edadMeses'] = baby_data['fechaDeNacimiento'].apply(lambda x: (datetime.now() - pd.to_datetime(x)).days // 30)
    characteristics_data = characteristics_data.merge(baby_data[['id_bebe', 'edadMeses']], left_on='bebe_id_bebe', right_on='id_bebe', how='left')
    
    # Gráfico de peso
    weights = characteristics_data['peso']
    ages = characteristics_data['edadMeses']
    expected_weights = [get_reference_weight(age, True)[1] for age in ages]
    
    fig_weight = go.Figure()
    fig_weight.add_trace(go.Scatter(x=ages, y=weights, mode='lines+markers', name='Peso Actual'))
    fig_weight.add_trace(go.Scatter(x=ages, y=expected_weights, mode='lines+markers', name='Peso Esperado'))
    fig_weight.update_layout(title="Comparación de Peso Actual vs Esperado", xaxis_title="Edad (meses)", yaxis_title="Peso (kg)")

    # Gráfico de altura
    heights = characteristics_data['altura']
    expected_heights = [get_reference_height(age, True) for age in ages]

    fig_height = go.Figure()
    fig_height.add_trace(go.Scatter(x=ages, y=heights, mode='lines+markers', name='Altura Actual'))
    fig_height.add_trace(go.Scatter(x=ages, y=expected_heights, mode='lines+markers', name='Altura Esperada'))
    fig_height.update_layout(title="Comparación de Altura Actual vs Esperada", xaxis_title="Edad (meses)", yaxis_title="Altura (cm)")

    return fig_weight, fig_height

# Hilo para ejecutar Dash
def run_dash():
    app.run_server(debug=True, use_reloader=False)

# Configuración de gráficos en Tkinter usando Matplotlib
def update_tkinter_charts():
    baby_data = get_baby_data()
    characteristics_data = get_characteristics_data()
    
    fig_weight.clear()
    fig_height.clear()

    # Gráfico de comparación de peso en Tkinter
    ax1 = fig_weight.add_subplot(111)
    characteristics_data = characteristics_data.merge(baby_data[['id_bebe', 'nombre']], left_on='bebe_id_bebe', right_on='id_bebe', how='left')
    ages = characteristics_data['edadMeses']
    weights = characteristics_data['peso']
    expected_weights = [get_reference_weight(age, True)[1] for age in ages]
    
    ax1.plot(ages, weights, 'o-', label='Peso Real')
    ax1.plot(ages, expected_weights, 'x--', label='Peso Esperado')
    ax1.set_title("Comparación de Peso en Tkinter")
    ax1.set_xlabel("Edad (meses)")
    ax1.set_ylabel("Peso (kg)")
    ax1.legend()

    # Gráfico de comparación de altura en Tkinter
    ax2 = fig_height.add_subplot(111)
    heights = characteristics_data['altura']
    expected_heights = [get_reference_height(age, True) for age in ages]
    
    ax2.plot(ages, heights, 'o-', label='Altura Real')
    ax2.plot(ages, expected_heights, 'x--', label='Altura Esperada')
    ax2.set_title("Comparación de Altura en Tkinter")
    ax2.set_xlabel("Edad (meses)")
    ax2.set_ylabel("Altura (cm)")
    ax2.legend()
    
    canvas_weight.draw()
    canvas_height.draw()

    # Refrescar cada 5 segundos
    root.after(5000, update_tkinter_charts)

# Configuración de la interfaz Tkinter
root = tk.Tk()
root.title("Dashboard de Cuna Inteligente")

# Botón para abrir el Dashboard de Dash en el navegador
def open_dashboard():
    webbrowser.open("http://127.0.0.1:8050")

tk.Button(root, text="Abrir Dashboard Interactivo", command=open_dashboard).pack()

# Gráficos en Tkinter
fig_weight = plt.Figure(figsize=(5, 4), dpi=100)
canvas_weight = FigureCanvasTkAgg(fig_weight, master=root)
canvas_weight.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

fig_height = plt.Figure(figsize=(5, 4), dpi=100)
canvas_height = FigureCanvasTkAgg(fig_height, master=root)
canvas_height.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Iniciar el dashboard de Dash en un hilo separado
threading.Thread(target=run_dash).start()

# Iniciar la actualización de los gráficos en Tkinter
update_tkinter_charts()
root.mainloop()