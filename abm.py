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
        # La ID es auto-incremental, no se incluye en los valores
        sql = "INSERT INTO bebe (nombre, apellidoPaterno, apellidoMaterno, fechaDeNacimiento, usuario_id_usuario) VALUES (%s, %s, %s, %s, %s)"
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
    elif tabla == "usuario":
        sql = "INSERT INTO usuario (username, nombre, apellidoPaterno, apellidoMaterno, gmail, contrasenia) VALUES (%s, %s, %s, %s, %s, %s)"
        if len(values) != 6:
            messagebox.showerror("Error", "Debe proporcionar exactamente 6 valores para la tabla 'usuario'.")
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

    if tabla == "registroTemperatura":
        sql = "DELETE FROM registroTemperatura WHERE id_registroTemp = %s"
    elif tabla == "registroHumedad":
        sql = "DELETE FROM registroHumedad WHERE id_registroHumedad = %s"
    elif tabla == "bebe":
        sql = "DELETE FROM bebe WHERE id_bebe = %s"
    elif tabla == "usuario":
        sql = "DELETE FROM usuario WHERE id_usuario = %s"

    try:
        cursor.execute(sql, (id_valor,))
        conn.commit()
        messagebox.showinfo("Operación Exitosa", "Registro eliminado con éxito")
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error al realizar la operación: {e}")
    finally:
        conn.close()

def modificacion(tabla, id_valor, new_values):
    conn = connect_db()
    cursor = conn.cursor()
    
    if tabla == "bebe":
        sql = "UPDATE bebe SET nombre = %s, apellidoPaterno = %s, apellidoMaterno = %s, fechaDeNacimiento = %s, usuario_id_usuario = %s WHERE id_bebe = %s"
    elif tabla == "registroTemperatura":
        sql = "UPDATE registroTemperatura SET temperatura = %s, fecha = %s, cuna_id_cuna = %s WHERE id_registroTemp = %s"
    elif tabla == "registroHumedad":
        sql = "UPDATE registroHumedad SET humedad = %s, fecha = %s, cuna_id_cuna = %s WHERE id_registroHumedad = %s"
    elif tabla == "usuario":
        sql = "UPDATE usuario SET username = %s, nombre = %s, apellidoPaterno = %s, apellidoMaterno = %s, gmail = %s, contrasenia = %s WHERE id_usuario = %s"
    
    try:
        cursor.execute(sql, (*new_values, id_valor))
        conn.commit()
        messagebox.showinfo("Operación Exitosa", "Registro actualizado con éxito")
    except Exception as e:
        messagebox.showerror("Error", f"Se produjo un error al realizar la operación: {e}")
    finally:
        conn.close()

def obtener_datos_bebe(id_bebe):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, apellidoPaterno, apellidoMaterno, fechaDeNacimiento, usuario_id_usuario FROM bebe WHERE id_bebe = %s", (id_bebe,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def obtener_datos_registro_temperatura(id_registroTemp):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT temperatura, fecha, cuna_id_cuna FROM registroTemperatura WHERE id_registroTemp = %s", (id_registroTemp,))
    datos_temperatura = cursor.fetchone()
    conn.close()
    return datos_temperatura

def obtener_datos_registro_humedad(id_registroHumedad):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT humedad, fecha, cuna_id_cuna FROM registroHumedad WHERE id_registroHumedad = %s", (id_registroHumedad,))
    datos_humedad = cursor.fetchone()
    conn.close()
    return datos_humedad

# Función para obtener datos específicos de un registro de usuario
def obtener_datos_usuario(id_usuario):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, nombre, apellidoPaterno, apellidoMaterno, gmail, contrasenia FROM usuario WHERE id_usuario = %s", (id_usuario,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

# Código para la interfaz de la tabla `registroTemperatura` y `registroHumedad`
def tabla_interfaz(tabla):
    def ejecutar_operacion():
        operacion = operacion_var.get()
        
        if operacion == "Alta":
            # Recolectamos los valores de las entradas según la tabla seleccionada
            if tabla == "bebe":
                values = (nombre_entry.get(), apellidoP_entry.get(), apellidoM_entry.get(), fechaNacimiento_entry.get(), id_usuario_entry.get())
            elif tabla == "registroTemperatura":
                values = (temperatura_entry.get(), fecha_entry.get(), cuna_id_entry.get())
            elif tabla == "registroHumedad":
                values = (humedad_entry.get(), fecha_entry.get(), cuna_id_entry.get())
            elif tabla == "usuario":
                values = (username_entry.get(), nombre_entry.get(), apellidoP_entry.get(), apellidoM_entry.get(), gmail_entry.get(), contrasenia_entry.get())            
            
            alta(tabla, values)
            
        elif operacion == "Baja":
            id_valor = id_entry.get()
            baja(tabla, id_valor)
        elif operacion == "Modificación":
            id_valor = id_entry.get()
            if tabla == "bebe":
                new_values = (nombre_entry.get(), apellidoP_entry.get(), apellidoM_entry.get(), fechaNacimiento_entry.get(), id_usuario_entry.get())
            elif tabla == "registroTemperatura":
                new_values = (temperatura_entry.get(), fecha_entry.get(), cuna_id_entry.get())
            elif tabla == "registroHumedad":
                new_values = (humedad_entry.get(), fecha_entry.get(), cuna_id_entry.get())
            elif tabla == "usuario":
                new_values = (username_entry.get(), nombre_entry.get(), apellidoP_entry.get(), apellidoM_entry.get(), gmail_entry.get(), contrasenia_entry.get())
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
            elif tabla == "registroHumedad":
                datos_humedad = obtener_datos_registro_humedad(id_valor)
                if datos_humedad:
                    humedad_entry.delete(0, END)
                    humedad_entry.insert(0, datos_humedad[0])
                    fecha_entry.delete(0, END)
                    fecha_entry.insert(0, datos_humedad[1])
                    cuna_id_entry.delete(0, END)
                    cuna_id_entry.insert(0, datos_humedad[2])
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
            if tabla == "usuario":
                datos_usuario = obtener_datos_usuario(id_valor)
                if datos_usuario:
                    username_entry.delete(0, END)
                    username_entry.insert(0, datos_usuario[0])
                    nombre_entry.delete(0, END)
                    nombre_entry.insert(0, datos_usuario[1])
                    apellidoP_entry.delete(0, END)
                    apellidoP_entry.insert(0, datos_usuario[2])
                    apellidoM_entry.delete(0, END)
                    apellidoM_entry.insert(0, datos_usuario[3])
                    gmail_entry.delete(0, END)
                    gmail_entry.insert(0, datos_usuario[4])
                    contrasenia_entry.delete(0, END)
                    contrasenia_entry.insert(0, datos_usuario[5])
                else:
                    messagebox.showwarning("No Encontrado", "No se encontraron datos para ese ID")

            
    ventana = Toplevel()
    ventana.title(f"Operaciones ABM para la tabla {tabla}")
    ventana.geometry("500x600")

    main_frame = ttk.Frame(ventana, padding=20)
    main_frame.pack(expand=True, fill=BOTH)

    operacion_var = StringVar(value="Alta")

    # Configuramos las entradas para cada tabla de acuerdo con el número de campos esperados
    if tabla == "bebe":
        entry_vars = [StringVar() for _ in range(5)]
    else:
        entry_vars = [StringVar() for _ in range(3)]
    
    ttk.Label(main_frame, text="Operación:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=W, pady=5)
    operacion_combo = ttk.Combobox(main_frame, textvariable=operacion_var, values=["Alta", "Baja", "Modificación"], state="readonly")
    operacion_combo.grid(row=0, column=1, padx=10)

    # Creamos el formulario según la tabla seleccionada
    if tabla == "bebe":
        ttk.Label(main_frame, text="ID (para Baja y Modificación):").grid(row=1, column=0, sticky=W, pady=5)
        id_entry = ttk.Entry(main_frame)
        id_entry.grid(row=1, column=1, padx=10)

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

        ttk.Label(main_frame, text="Fecha de Nacimiento").grid(row=5, column=0, sticky=W, pady=5)
        fechaNacimiento_entry = ttk.Entry(main_frame, textvariable=entry_vars[3])
        fechaNacimiento_entry.grid(row=5, column=1, padx=10)

        ttk.Label(main_frame, text="ID Usuario").grid(row=6, column=0, sticky=W, pady=5)
        id_usuario_entry = ttk.Entry(main_frame, textvariable=entry_vars[4])
        id_usuario_entry.grid(row=6, column=1, padx=10)
    
    elif tabla == "registroTemperatura":
        ttk.Label(main_frame, text="ID (para Baja y Modificación):").grid(row=1, column=0, sticky=W, pady=5)
        id_entry = ttk.Entry(main_frame)
        id_entry.grid(row=1, column=1, padx=10)

        autocompletar_btn = ttk.Button(main_frame, text="Autocompletar", command=autocompletar_campos, style='info.TButton')
        autocompletar_btn.grid(row=1, column=2, padx=10)

        ttk.Label(main_frame, text="Temperatura").grid(row=2, column=0, sticky=W, pady=5)
        temperatura_entry = ttk.Entry(main_frame)
        temperatura_entry.grid(row=2, column=1, padx=10)

        ttk.Label(main_frame, text="Fecha").grid(row=3, column=0, sticky=W, pady=5)
        fecha_entry = ttk.Entry(main_frame)
        fecha_entry.grid(row=3, column=1, padx=10)

        ttk.Label(main_frame, text="ID Cuna").grid(row=4, column=0, sticky=W, pady=5)
        cuna_id_entry = ttk.Entry(main_frame)
        cuna_id_entry.grid(row=4, column=1, padx=10)
        
    elif tabla == "registroHumedad":
        ttk.Label(main_frame, text="ID (para Baja y Modificación):").grid(row=1, column=0, sticky=W, pady=5)
        id_entry = ttk.Entry(main_frame)
        id_entry.grid(row=1, column=1, padx=10)

        autocompletar_btn = ttk.Button(main_frame, text="Autocompletar", command=autocompletar_campos, style='info.TButton')
        autocompletar_btn.grid(row=1, column=2, padx=10)

        ttk.Label(main_frame, text="Humedad").grid(row=2, column=0, sticky=W, pady=5)
        humedad_entry = ttk.Entry(main_frame)
        humedad_entry.grid(row=2, column=1, padx=10)

        ttk.Label(main_frame, text="Fecha").grid(row=3, column=0, sticky=W, pady=5)
        fecha_entry = ttk.Entry(main_frame)
        fecha_entry.grid(row=3, column=1, padx=10)

        ttk.Label(main_frame, text="ID Cuna").grid(row=4, column=0, sticky=W, pady=5)
        cuna_id_entry = ttk.Entry(main_frame)
        cuna_id_entry.grid(row=4, column=1, padx=10)
    
    elif tabla == "usuario":
        ttk.Label(main_frame, text="ID (para Baja y Modificación):").grid(row=1, column=0, sticky=W, pady=5)
        id_entry = ttk.Entry(main_frame)
        id_entry.grid(row=1, column=1, padx=10)

        autocompletar_btn = ttk.Button(main_frame, text="Autocompletar", command=autocompletar_campos, style='info.TButton')
        autocompletar_btn.grid(row=1, column=2, padx=10)

        ttk.Label(main_frame, text="Username").grid(row=2, column=0, sticky=W, pady=5)
        username_entry = ttk.Entry(main_frame)
        username_entry.grid(row=2, column=1, padx=10)

        ttk.Label(main_frame, text="Nombre").grid(row=3, column=0, sticky=W, pady=5)
        nombre_entry = ttk.Entry(main_frame)
        nombre_entry.grid(row=3, column=1, padx=10)

        ttk.Label(main_frame, text="Apellido Paterno").grid(row=4, column=0, sticky=W, pady=5)
        apellidoP_entry = ttk.Entry(main_frame)
        apellidoP_entry.grid(row=4, column=1, padx=10)

        ttk.Label(main_frame, text="Apellido Materno").grid(row=5, column=0, sticky=W, pady=5)
        apellidoM_entry = ttk.Entry(main_frame)
        apellidoM_entry.grid(row=5, column=1, padx=10)

        ttk.Label(main_frame, text="Gmail").grid(row=6, column=0, sticky=W, pady=5)
        gmail_entry = ttk.Entry(main_frame)
        gmail_entry.grid(row=6, column=1, padx=10)

        ttk.Label(main_frame, text="Contraseña").grid(row=7, column=0, sticky=W, pady=5)
        contrasenia_entry = ttk.Entry(main_frame, show="*")
        contrasenia_entry.grid(row=7, column=1, padx=10)

    ejecutar_btn = ttk.Button(main_frame, text="Ejecutar", command=ejecutar_operacion, style='primary.TButton')
    ejecutar_btn.grid(row=10, column=1, pady=20)

def abrir_pantalla_principal():
    ventana_principal = Tk()
    ventana_principal.title("Cuna Inteligente - ABM")
    ventana_principal.geometry("400x300")

    style = Style()
    style.theme_use('minty')

    main_frame = ttk.Frame(ventana_principal, padding=20)
    main_frame.pack(expand=True, fill=BOTH)

    ttk.Label(main_frame, text="Gestión de la Cuna Inteligente", font=("Arial", 16, "bold")).pack(pady=10)
    
    bebe_btn = ttk.Button(main_frame, text="Gestión de Bebé", command=lambda: tabla_interfaz("bebe"), style='primary.TButton')
    bebe_btn.pack(fill=BOTH, pady=5)

    temp_btn = ttk.Button(main_frame, text="Registro de Temperatura", command=lambda: tabla_interfaz("registroTemperatura"), style='primary.TButton')
    temp_btn.pack(fill=BOTH, pady=5)

    humedad_btn = ttk.Button(main_frame, text="Registro de Humedad", command=lambda: tabla_interfaz("registroHumedad"), style='primary.TButton')
    humedad_btn.pack(fill=BOTH, pady=5)
    
    usuario_btn = ttk.Button(main_frame, text="Registro de Usuario", command=lambda: tabla_interfaz("usuario"), style='primary.TButton')
    usuario_btn.pack(fill=BOTH, pady=5)

    ventana_principal.mainloop()

abrir_pantalla_principal()
