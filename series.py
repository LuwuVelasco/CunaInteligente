import network
import urequests as requests
import ujson
import math
import random
import time
from machine import Pin

# Conexión a Wi-Fi
ssid = "tu_ssid"
password = "tu_password"
url = "http://192.168.6.190/insert_data.php"  # URL del script PHP

# Configuración de Wi-Fi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    time.sleep(1)
    print("Conectando a Wi-Fi...")

print("Conectado:", station.ifconfig())

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

# Función de Fourier para seno
def serie_fourier_seno(x, nmax):
    sumatoria = 0
    for n in range(1, nmax + 1):
        termino = (2 / (n * math.pi)) * (1 - (-1)**n) * math.sin(n * x)
        sumatoria += termino
    return sumatoria

# Función para generar la Serie de Fibonacci
def serie_fibonacci(nmax):
    fibonacci_vals = [0, 1]
    while len(fibonacci_vals) < nmax:
        next_val = fibonacci_vals[-1] + fibonacci_vals[-2]
        fibonacci_vals.append(next_val)
    return fibonacci_vals[:nmax]

# Generación de valores con ruido
def generar_valores_con_ruido(num_puntos, nmax, funcion, es_fibonacci=False):
    x_vals = []
    original_vals = []
    ruido_vals = []
    error_vals = []

    if es_fibonacci:
        # Si es la Serie de Fibonacci, no necesitamos el parámetro `x`
        original_vals = funcion(nmax)
        for i in range(len(original_vals)):
            ruido = random.uniform(-0.1, 0.1) * abs(original_vals[i])
            y_con_ruido = original_vals[i] + ruido
            error = abs(y_con_ruido - original_vals[i])
            ruido_vals.append(y_con_ruido)
            error_vals.append(error)
        return list(range(len(original_vals))), original_vals, ruido_vals, error_vals
    
    # Para series de Taylor y Fourier
    for i in range(num_puntos):
        x = i * (2 * math.pi / num_puntos)
        y_original = funcion(x, nmax)
        
        ruido = random.uniform(-0.1, 0.1) * abs(y_original)
        y_con_ruido = y_original + ruido
        error = abs(y_con_ruido - y_original)
        
        x_vals.append(x)
        original_vals.append(y_original)
        ruido_vals.append(y_con_ruido)
        error_vals.append(error)
    
    return x_vals, original_vals, ruido_vals, error_vals

# Envío de datos al servidor
def enviar_datos_serie(serie, nmax, puntos, es_fibonacci=False):
    x_vals, original_vals, ruido_vals, error_vals = generar_valores_con_ruido(puntos, nmax, serie, es_fibonacci)

    for i in range(len(original_vals)):
        data = {
            "x": x_vals[i],
            "original": original_vals[i],
            "con_ruido": ruido_vals[i],
            "error": error_vals[i]
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=ujson.dumps(data), headers=headers)
        print("Datos enviados:", data)
        print("Respuesta del servidor:", response.text)
        response.close()
        time.sleep(1)

# Configuración inicial de la serie y valores
num_puntos = 10  # Número de puntos para calcular en la serie
nmax = 5  # Número de términos en la serie de Taylor o Fourier

# Enviar valores de cada serie
print("Enviando serie de Taylor (Coseno)...")
enviar_datos_serie(serie_taylor_coseno, nmax, num_puntos)

print("Enviando serie de Taylor (Seno)...")
enviar_datos_serie(serie_taylor_seno, nmax, num_puntos)

print("Enviando serie de Fourier (Seno)...")
enviar_datos_serie(serie_fourier_seno, nmax, num_puntos)

print("Enviando serie de Fibonacci...")
enviar_datos_serie(serie_fibonacci, nmax, num_puntos, es_fibonacci=True)
