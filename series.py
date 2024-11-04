import network
import urequests as requests
import ujson
import math
import random
import time
from machine import Pin
from Wifi_lib import wifi_init  # Importar Wifi_lib para manejar la conexión Wi-Fi

url = "http://192.168.6.190/registrocaracteristicas.php"  # URL del script PHP
# Inicializar la conexión Wi-Fi
station = wifi_init()  # Usar Wifi_lib para conectarse

# Configuración de pines para los LEDs y botones
led_verde = Pin(5, Pin.OUT)
led_azul = Pin(17, Pin.OUT)
led_rojo = Pin(18, Pin.OUT)

btn_apagar = Pin(33, Pin.IN, Pin.PULL_UP)  # Pulsador para apagar LEDs (GPIO 33)
btn_rojo = Pin(32, Pin.IN, Pin.PULL_UP)    # Pulsador para LED rojo (GPIO 32)
btn_verde = Pin(25, Pin.IN, Pin.PULL_UP)   # Pulsador para LED verde (GPIO 25)
btn_azul = Pin(26, Pin.IN, Pin.PULL_UP)    # Pulsador para LED azul (GPIO 26)

# Función para apagar todos los LEDs
def apagar_leds():
    led_rojo.value(0)
    led_verde.value(0)
    led_azul.value(0)

# Función de Taylor para coseno
def serie_taylor_coseno(x, nmax):
    sumatoria = 0
    for n in range(nmax + 1):
        termino = ((-1)**n * (x**(2 * n))) / math.factorial(2 * n)
        sumatoria += termino
    return sumatoria

# Función de Taylor para seno
def serie_taylor_seno(x, nmax):
    sumatoria = 0
    for n in range(nmax + 1):
        termino = ((-1)**n * (x**(2 * n + 1))) / math.factorial(2 * n + 1)
        sumatoria += termino
    return sumatoria

# Generación de valores con ruido
def generar_valores_con_ruido(num_puntos, nmax, funcion):
    x_vals = []
    original_vals = []
    ruido_vals = []

    for i in range(num_puntos):
        x = i * (2 * math.pi / num_puntos)
        y_original = funcion(x, nmax)
        
        ruido = random.uniform(-0.1, 0.1) * abs(y_original)
        y_con_ruido = y_original + ruido
        
        x_vals.append(x)
        original_vals.append(y_original)
        ruido_vals.append(y_con_ruido)
    
    return x_vals, original_vals, ruido_vals

# Envío de datos al servidor
def enviar_datos(peso, altura, id_registro, fecha, bebe_id):
    data = {
        "id_registroCaracteristicas": id_registro,
        "fecha": fecha,
        "peso": peso,
        "altura": altura,
        "bebe_id_bebe": bebe_id
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=ujson.dumps(data), headers=headers)
    print("Datos enviados:", data)
    print("Respuesta del servidor:", response.text)
    response.close()
    time.sleep(1)

# Configuración inicial
num_puntos = 10  # Número de puntos para calcular en la serie
nmax = 5  # Número de términos en la serie de Taylor
bebe_id = 1  # ID de ejemplo para el bebé
fecha = "2024-11-03"  # Fecha de ejemplo (puedes modificarla para obtener la fecha actual)

# Generar valores para coseno y seno con ruido
x_vals, cos_vals, cos_ruido_vals = generar_valores_con_ruido(num_puntos, nmax, serie_taylor_coseno)
_, sen_vals, sen_ruido_vals = generar_valores_con_ruido(num_puntos, nmax, serie_taylor_seno)

# Función para enviar las series al servidor
def enviar_series():
    for i in range(num_puntos):
        id_registro = i + 1  # ID de registro único para cada punto
        peso = cos_ruido_vals[i]  # Usar el valor con ruido de coseno como peso
        altura = sen_ruido_vals[i]  # Usar el valor con ruido de seno como altura
        enviar_datos(peso, altura, id_registro, fecha, bebe_id)

# Bucle principal para detectar la pulsación de botones y enviar datos
while True:
    if btn_apagar.value() == 0:
        apagar_leds()
        print("Botón apagar presionado")
        enviar_series()

    elif btn_rojo.value() == 0:
        apagar_leds()
        led_rojo.value(1)
        print("Botón rojo presionado")
        enviar_series()

    elif btn_verde.value() == 0:
        apagar_leds()
        led_verde.value(1)
        print("Botón verde presionado")
        enviar_series()

    elif btn_azul.value() == 0:
        apagar_leds()
        led_azul.value(1)
        print("Botón azul presionado")
        enviar_series()

    # Pequeño retardo para evitar múltiples lecturas de una misma pulsación
    time.sleep(0.1)
