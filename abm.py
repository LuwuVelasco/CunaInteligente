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
        # Si 'id_bebe' es autoincrementable, no lo incluyas en los valores
        sql = "INSERT INTO bebe (nombre, apellidoPaterno, apellidoMaterno, fechaDeNacimiento, usuario_id_usuario) VALUES (%s, %s, %s, %s, %s)"
        # Asegúrate de pasar 5 valores en lugar de 6, ya que 'id_bebe' es autoincrementable
        if len(values) != 5:
            messagebox.showerror("Error", "Debe proporcionar exactamente 5 valores para la tabla 'bebe'.")
            return
    elif tabla == "registroTemperatura":
        sql = "INSERT INTO registroTemperatura (temperatura, fecha, cuna_id_cuna) VALUES (%s, %s, %s)"
        if len(values) != 3:
            messagebox.showerror("Error", "Debe proporcionar exactamente 3 valores para la tabla 'registroTemperatura'.")
            return
    elif tabla == "registroHumedad":
        sql = "INSERT INTO registroHumedad (humedad, fecha, cuna_id_cuna) VALUES (%s, %s, %s)"
        if len(values) != 3:
            messagebox.showerror("Error", "Debe proporcionar exactamente 3 valores para la tabla 'registroHumedad'.")
            return
    
    try:
        cursor.execute(sql, values)
        conn.commit()
        messagebox.showinfo("Operación Exitosa", "Registro agregado con éxito")
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error al realizar la operación: {e}")
    finally:
        conn.close()

def baja(tabla, id_valor):
    conn = connect_db()
    cursor = conn.cursor()

    # Aquí asegúrate de que el nombre de la columna en WHERE coincida con la estructura de tu base de datos
    if tabla == "registroTemperatura":
        sql = "DELETE FROM registroTemperatura WHERE id_registroTemp = %s"
    elif tabla == "registroHumedad":
        sql = "DELETE FROM registroHumedad WHERE id_registroHumedad = %s"
    elif tabla == "bebe":
        sql = "DELETE FROM bebe WHERE id_bebe = %s"

    cursor.execute(sql, (id_valor,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Operación Exitosa", "Registro eliminado con éxito")


def modificacion(tabla, id_valor, new_values):
    conn = connect_db()
    cursor = conn.cursor()
    
    if tabla == "bebe":
        sql = "UPDATE bebe SET nombre = %s, apellidoPaterno = %s, apellidoMaterno = %s, fechaDeNacimiento = %s, usuario_id_usuario = %s WHERE id_bebe = %s"
    elif tabla == "registroTemperatura":
        sql = "UPDATE registroTemperatura SET temperatura = %s, fecha = %s WHERE id_registroTemp = %s"
    elif tabla == "registroHumedad":
        sql = "UPDATE registroHumedad SET humedad = %s, fecha = %s WHERE id_registroHumedad = %s"
    
    cursor.execute(sql, (*new_values, id_valor))
    conn.commit()
    conn.close()
    messagebox.showinfo("Operación Exitosa", "Registro actualizado con éxito")

# Función para obtener los datos de un bebé por ID
def obtener_datos_bebe(id_bebe):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, apellidoPaterno, apellidoMaterno, fechaDeNacimiento, usuario_id_usuario FROM bebe WHERE id_bebe = %s", (id_bebe,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

# Función para obtener los datos de un registro de temperatura por ID
def obtener_datos_registro_temperatura(id_registroTemp):
    # Consulta actualizada con el nombre correcto de la columna
    query = "SELECT temperatura, fecha, cuna_id_cuna FROM registroTemperatura WHERE id_registroTemp = %s"
    
    # Usar la función de conexión
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, (id_registroTemp,))
    datos_temperatura = cursor.fetchone()
    
    if datos_temperatura:
        return datos_temperatura
    else:
        return None



# Interfaz para cada tabla
def tabla_interfaz(tabla):
    def ejecutar_operacion():
        operacion = operacion_var.get()
        
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

    def autocompletar_campos():
        id_valor = id_entry.get()
        if id_valor:
            if tabla == "registroTemperatura":
                datos_temperatura = obtener_datos_registro_temperatura(id_valor)
                if datos_temperatura:
                    temperatura_entry.delete(0, END)
                    temperatura_entry.insert(0, datos_temperatura[0])
                    fecha_entry.delete(0, END)
                    fecha_entry.insert(0, datos_temperatura[1])
                    cuna_id_entry.delete(0, END)
                    cuna_id_entry.insert(0, datos_temperatura[2])
                else:
                    messagebox.showwarning("No Encontrado", "No se encontraron datos para ese ID")
            elif tabla == "bebe":
                datos_bebe = obtener_datos_bebe(id_valor)
                if datos_bebe:
                    nombre_entry.delete(0, END)
                    nombre_entry.insert(0, datos_bebe[0])
                    apellidoP_entry.delete(0, END)
                    apellidoP_entry.insert(0, datos_bebe[1])
                    apellidoM_entry.delete(0, END)
                    apellidoM_entry.insert(0, datos_bebe[2])
                    fechaNacimiento_entry.delete(0, END)
                    fechaNacimiento_entry.insert(0, datos_bebe[3])
                    id_usuario_entry.delete(0, END)
                    id_usuario_entry.insert(0, datos_bebe[4])
                else:
                    messagebox.showwarning("No Encontrado", "No se encontraron datos para ese ID")

    # Crear una nueva ventana para la tabla seleccionada
    ventana = Toplevel()
    ventana.title(f"Operaciones ABM para la tabla {tabla}")
    ventana.geometry("500x600")

    main_frame = ttk.Frame(ventana, padding=20)
    main_frame.pack(expand=True, fill=BOTH)

    operacion_var = StringVar(value="Alta")
    entry_vars = [StringVar() for _ in range(5)]

    ttk.Label(main_frame, text="Operación:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=W, pady=5)
    operacion_combo = ttk.Combobox(main_frame, textvariable=operacion_var, values=["Alta", "Baja", "Modificación"], state="readonly")
    operacion_combo.grid(row=0, column=1, padx=10)

    # Campos específicos por tabla
    if tabla == "bebe":
        ttk.Label(main_frame, text="ID (para Baja y Modificación):").grid(row=1, column=0, sticky=W, pady=5)
        id_entry = ttk.Entry(main_frame)
        id_entry.grid(row=1, column=1, padx=10)
        
        # Botón para autocompletar
        autocompletar_btn = ttk.Button(main_frame, text="Autocompletar", command=autocompletar_campos, style='info.TButton')
        autocompletar_btn.grid(row=1, column=2, padx=10)

        ttk.Label(main_frame, text="Nombre").grid(row=2, column=0, sticky=W, pady=5)
        nombre_entry = ttk.Entry(main_frame, textvariable=entry_vars[0])
        nombre_entry.grid(row=2, column=1, padx=10)

        ttk.Label(main_frame, text="Apellido Paterno").grid(row=3, column=0, sticky=W, pady=5)
        apellidoP_entry = ttk.Entry(main_frame, textvariable=entry_vars[1])
        apellidoP_entry.grid(row=3, column=1, padx=10)

        ttk.Label(main_frame, text="Apellido Materno").grid(row=4, column=0, sticky=W, pady=5)
        apellidoM_entry = ttk.Entry(main_frame, textvariable=entry_vars[2])
        apellidoM_entry.grid(row=4, column=1, padx=10)

        ttk.Label(main_frame, text="Fecha de Nacimiento (YYYY-MM-DD)").grid(row=5, column=0, sticky=W, pady=5)
        fechaNacimiento_entry = ttk.Entry(main_frame, textvariable=entry_vars[3])
        fechaNacimiento_entry.grid(row=5, column=1, padx=10)

        ttk.Label(main_frame, text="ID Usuario").grid(row=6, column=0, sticky=W, pady=5)
        id_usuario_entry = ttk.Entry(main_frame, textvariable=entry_vars[4])
        id_usuario_entry.grid(row=6, column=1, padx=10)

    elif tabla == "registroTemperatura":
        ttk.Label(main_frame, text="ID (para Baja y Modificación):").grid(row=1, column=0, sticky=W, pady=5)
        id_entry = ttk.Entry(main_frame)
        id_entry.grid(row=1, column=1, padx=10)
        
        # Botón para autocompletar
        autocompletar_btn = ttk.Button(main_frame, text="Autocompletar", command=autocompletar_campos, style='info.TButton')
        autocompletar_btn.grid(row=1, column=2, padx=10)

        ttk.Label(main_frame, text="Temperatura").grid(row=2, column=0, sticky=W, pady=5)
        temperatura_entry = ttk.Entry(main_frame, textvariable=entry_vars[0])
        temperatura_entry.grid(row=2, column=1, padx=10)

        ttk.Label(main_frame, text="Fecha").grid(row=3, column=0, sticky=W, pady=5)
        fecha_entry = ttk.Entry(main_frame, textvariable=entry_vars[1])
        fecha_entry.grid(row=3, column=1, padx=10)

        # Nuevo campo para cuna_id_cuna
        ttk.Label(main_frame, text="Cuna ID").grid(row=4, column=0, sticky=W, pady=5)
        cuna_id_entry = ttk.Entry(main_frame, textvariable=entry_vars[2])
        cuna_id_entry.grid(row=4, column=1, padx=10)

    # Botón para ejecutar la operación
    ejecutar_btn = ttk.Button(main_frame, text="Ejecutar Operación", command=ejecutar_operacion)
    ejecutar_btn.grid(row=7, columnspan=3, pady=10)

    ventana.mainloop()

# Función principal para la ventana principal
def ventana_principal():
    ventana = Tk()
    ventana.title("Gestión de Base de Datos Cuna Inteligente")
    ventana.geometry("400x400")

    ttk.Button(ventana, text="Gestión de Bebé", command=lambda: tabla_interfaz("bebe")).pack(pady=20)
    ttk.Button(ventana, text="Gestión de Temperaturas", command=lambda: tabla_interfaz("registroTemperatura")).pack(pady=20)
    ttk.Button(ventana, text="Gestión de Humedad", command=lambda: tabla_interfaz("registroHumedad")).pack(pady=20)

    ventana.mainloop()

# Iniciar la aplicación
ventana_principal()


