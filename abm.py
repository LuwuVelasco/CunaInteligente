import mysql.connector
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from tkinter import *
from tkinter import messagebox, ttk

# Configuración de la conexión a la base de datos MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cunainteligente"
    )

# Funciones de Alta, Baja y Modificación
def alta(tabla, values):
    conn = connect_db()
    cursor = conn.cursor()
    
    if tabla == "bebe":
        sql = "INSERT INTO bebe (nombre, apellidoPaterno, apellidoMaterno, fechaDeNacimiento, id_usuario) VALUES (%s, %s, %s, %s, %s)"
    elif tabla == "registroTemperatura":
        sql = "INSERT INTO registroTemperatura (temperatura, fecha, id_bebe) VALUES (%s, %s, %s)"
    elif tabla == "registroHumedad":
        sql = "INSERT INTO registroHumedad (humedad, fecha, id_bebe) VALUES (%s, %s, %s)"
    
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    messagebox.showinfo("Operación Exitosa", "Registro agregado con éxito")

def baja(tabla, id_valor):
    conn = connect_db()
    cursor = conn.cursor()
    sql = f"DELETE FROM {tabla} WHERE id_{tabla} = %s"
    cursor.execute(sql, (id_valor,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Operación Exitosa", "Registro eliminado con éxito")

def modificacion(tabla, id_valor, new_values):
    conn = connect_db()
    cursor = conn.cursor()
    
    if tabla == "bebe":
        sql = "UPDATE bebe SET nombre = %s, apellidoPaterno = %s, apellidoMaterno = %s, fechaDeNacimiento = %s, id_usuario = %s WHERE id_bebe = %s"
        values = (*new_values, id_valor)  # Desempaquetamos `new_values` y agregamos `id_valor` al final
    elif tabla == "registroTemperatura":
        sql = "UPDATE registroTemperatura SET temperatura = %s, fecha = %s WHERE id_registroTemp = %s"
        values = (*new_values, id_valor)
    elif tabla == "registroHumedad":
        sql = "UPDATE registroHumedad SET humedad = %s, fecha = %s WHERE id_registroHumedad = %s"
        values = (*new_values, id_valor)
    
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    messagebox.showinfo("Operación Exitosa", "Registro actualizado con éxito")



# Interfaz gráfica con ttkbootstrap
def interfaz():
    root = Tk()
    style = Style(theme='cosmo')
    root.title("Sistema ABM para Cuna Inteligente")
    root.geometry("500x700")
    root.configure(bg=style.colors.primary)

    # Crear marco principal
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(expand=True, fill=BOTH)

    # Variables y widgets de entrada
    operacion_var = StringVar(value="Alta")
    tabla_var = StringVar(value="bebe")
    entry_vars = [StringVar() for _ in range(5)]

    # Función para manejar las operaciones
    def ejecutar_operacion():
        operacion = operacion_var.get()
        tabla = tabla_var.get()
        
        if operacion == "Alta":
            values = tuple(entry_var.get() for entry_var in entry_vars)
            alta(tabla, values)
        elif operacion == "Baja":
            id_valor = id_entry.get()
            baja(tabla, id_valor)
        elif operacion == "Modificación":
            id_valor = id_entry.get()
            if tabla == "bebe":
                new_values = (nombre_entry.get(), apellidoP_entry.get(), apellidoM_entry.get(), fechaNacimiento_entry.get(), id_usuario_entry.get())
            elif tabla == "registroTemperatura":
                new_values = (temperatura_entry.get(), fecha_entry.get())
            elif tabla == "registroHumedad":
                new_values = (humedad_entry.get(), fecha_entry.get())
            modificacion(tabla, id_valor, new_values)

    # Etiquetas y widgets de selección
    ttk.Label(main_frame, text="Operación:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=W, pady=5)
    operacion_combo = ttk.Combobox(main_frame, textvariable=operacion_var, values=["Alta", "Baja", "Modificación"], state="readonly")
    operacion_combo.grid(row=0, column=1, padx=10)

    ttk.Label(main_frame, text="Tabla:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky=W, pady=5)
    tabla_combo = ttk.Combobox(main_frame, textvariable=tabla_var, values=["bebe", "registroTemperatura", "registroHumedad"], state="readonly")
    tabla_combo.grid(row=1, column=1, padx=10)

    # Entradas para el ID (solo Baja y Modificación)
    ttk.Label(main_frame, text="ID (para Baja y Modificación):", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky=W, pady=5)
    id_entry = ttk.Entry(main_frame)
    id_entry.grid(row=2, column=1, padx=10)

    # Entradas específicas para la tabla `bebe`
    ttk.Label(main_frame, text="Nombre").grid(row=3, column=0, sticky=W, pady=5)
    nombre_entry = ttk.Entry(main_frame, textvariable=entry_vars[0])
    nombre_entry.grid(row=3, column=1, padx=10)

    ttk.Label(main_frame, text="Apellido Paterno").grid(row=4, column=0, sticky=W, pady=5)
    apellidoP_entry = ttk.Entry(main_frame, textvariable=entry_vars[1])
    apellidoP_entry.grid(row=4, column=1, padx=10)

    ttk.Label(main_frame, text="Apellido Materno").grid(row=5, column=0, sticky=W, pady=5)
    apellidoM_entry = ttk.Entry(main_frame, textvariable=entry_vars[2])
    apellidoM_entry.grid(row=5, column=1, padx=10)

    ttk.Label(main_frame, text="Fecha de Nacimiento (YYYY-MM-DD)").grid(row=6, column=0, sticky=W, pady=5)
    fechaNacimiento_entry = ttk.Entry(main_frame, textvariable=entry_vars[3])
    fechaNacimiento_entry.grid(row=6, column=1, padx=10)

    ttk.Label(main_frame, text="ID Usuario").grid(row=7, column=0, sticky=W, pady=5)
    id_usuario_entry = ttk.Entry(main_frame, textvariable=entry_vars[4])
    id_usuario_entry.grid(row=7, column=1, padx=10)

    # Entradas para `registroTemperatura` y `registroHumedad`
    ttk.Label(main_frame, text="Temperatura (para registroTemperatura)").grid(row=8, column=0, sticky=W, pady=5)
    temperatura_entry = ttk.Entry(main_frame)
    temperatura_entry.grid(row=8, column=1, padx=10)

    ttk.Label(main_frame, text="Fecha (para registroTemperatura y registroHumedad)").grid(row=9, column=0, sticky=W, pady=5)
    fecha_entry = ttk.Entry(main_frame)
    fecha_entry.grid(row=9, column=1, padx=10)

    ttk.Label(main_frame, text="Humedad (para registroHumedad)").grid(row=10, column=0, sticky=W, pady=5)
    humedad_entry = ttk.Entry(main_frame)
    humedad_entry.grid(row=10, column=1, padx=10)

    # Botón para ejecutar la operación
    ejecutar_btn = ttk.Button(main_frame, text="Ejecutar Operación", command=ejecutar_operacion, style='success.TButton')
    ejecutar_btn.grid(row=11, column=0, columnspan=2, pady=20)

    root.mainloop()

# Ejecutar la interfaz
if __name__ == "__main__":
    interfaz()
