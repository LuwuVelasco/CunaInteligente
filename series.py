import network
import urequests as requests
import ujson
import math
import random
import time
from machine import Pin
from Wifi_lib import wifi_init  # Importar Wifi_lib para manejar la conexión Wi-Fi

# URLs de los scripts PHP para registrar humedad y temperatura
url_humedad = "http://192.168.37.84/CunaInteligente/registroHumedad.php"
url_temperatura = "http://192.168.37.84/CunaInteligente/registroTemperatura.php"

# Inicializar la conexión Wi-Fi
station = wifi_init()  # Usar Wifi_lib para conectarse

# Configuración de pines para los LEDs y botones
led_verde = Pin(5, Pin.OUT)
led_azul = Pin(17, Pin.OUT)
led_rojo = Pin(18, Pin.OUT)

btn_humedad = Pin(32, Pin.IN, Pin.PULL_UP)    # Pulsador para registrar humedad (GPIO 32)
btn_temperatura = Pin(33, Pin.IN, Pin.PULL_UP) # Pulsador para registrar temperatura (GPIO 33)

# Función para apagar todos los LEDs
def apagar_leds():
    led_rojo.value(0)
    led_verde.value(0)
    led_azul.value(0)

# Función de Taylor para coseno
def serie_taylor_coseno(x, nmax):
    sumatoria = 0
    for n in range(nmax + 1):
        termino = ((-1) ** n * (x ** (2 * n))) / math.factorial(2 * n)
        sumatoria += termino
    return sumatoria

# Función de Taylor para seno
def serie_taylor_seno(x, nmax):
    sumatoria = 0
    for n in range(nmax + 1):
        termino = ((-1) ** n * (x ** (2 * n + 1))) / math.factorial(2 * n + 1)
        sumatoria += termino
    return sumatoria

# Función para enviar datos de temperatura
def enviar_temperatura(temperatura, fecha, id_cuna):
    data = {
        "temperatura": temperatura,
        "fecha": fecha,
        "cuna_id_cuna": id_cuna
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url_temperatura, data=ujson.dumps(data), headers=headers)
    print("Datos de temperatura enviados:", data)
    print("Respuesta del servidor:", response.text)
    response.close()

# Función para enviar datos de humedad
def enviar_humedad(humedad, fecha, id_cuna):
    data = {
        "humedad": humedad,
        "fecha": fecha,
        "cuna_id_cuna": id_cuna
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url_humedad, data=ujson.dumps(data), headers=headers)
    print("Datos de humedad enviados:", data)
    print("Respuesta del servidor:", response.text)
    response.close()

# Función para obtener el ID de la cuna
def obtener_id_cuna():
    # Simulación de IDs válidos, puedes reemplazarlo con una consulta al servidor
    ids_disponibles = [1, 2, 3]  # Lista de IDs de ejemplo
    while True:
        try:
            cuna_id = int(input("Por favor, introduce el ID de la cuna: "))
            if cuna_id in ids_disponibles:
                return cuna_id
            else:
                print("ID de cuna no disponible. Inténtalo de nuevo.")
        except ValueError:
            print("Entrada inválida. Por favor, introduce un número entero.")

# Configuración inicial
num_puntos = 50  # Número de puntos para calcular en la serie
nmax = 10  # Número de términos en la serie de Taylor
valores_x = [i * (2 * math.pi) / num_puntos for i in range(num_puntos)]  # Genera puntos de 0 a 2π
indice = 0  # Índice inicial para recorrer valores_x

# Obtener ID de la cuna antes de iniciar el bucle
cuna_id = obtener_id_cuna()

# Obtener la fecha actual en el formato adecuado
def obtener_fecha_formateada():
    tiempo = time.localtime()
    return f"{tiempo[0]:04d}-{tiempo[1]:02d}-{tiempo[2]:02d} {tiempo[3]:02d}:{tiempo[4]:02d}:{tiempo[5]:02d}"

fecha = obtener_fecha_formateada()  # Obtener la fecha actual

# Bucle principal para detectar la pulsación de botones y enviar datos

# Bucle principal para detectar la pulsación de botones y enviar datos
while True:
    if btn_temperatura.value() == 0:
        apagar_leds()
        led_rojo.value(1)
        print("Botón de temperatura presionado")
        
        # Usar el siguiente valor en valores_x para coseno
        temperatura = serie_taylor_coseno(valores_x[indice], nmax)
        enviar_temperatura(temperatura, fecha, cuna_id)

        # Avanzar al siguiente índice, reiniciar si alcanza el final del vector
        indice = (indice + 1) % num_puntos

    elif btn_humedad.value() == 0:
        apagar_leds()
        led_verde.value(1)
        print("Botón de humedad presionado")
        
        # Usar el siguiente valor en valores_x para seno
        humedad = serie_taylor_seno(valores_x[indice], nmax)
        enviar_humedad(humedad, fecha, cuna_id)

        # Avanzar al siguiente índice, reiniciar si alcanza el final del vector
        indice = (indice + 1) % num_puntos

    # Pequeño retardo para evitar múltiples lecturas de una misma pulsación
    time.sleep(0.1)
