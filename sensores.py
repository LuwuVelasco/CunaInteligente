from machine import Pin, PWM
from time import sleep_ms  # Pausa en milisegundos
from Wifi_lib import wifi_init  # Import Wifi_lib for Wi-Fi connection
import time
import dht
import sys
import os
import network
import urequests as requests
import ujson
import math
import random
# Configurar PWM en el pin GPIO 25
servo_pin = PWM(Pin(25), freq=50)
data_pin = 16
dht_sensor = dht.DHT22(Pin(data_pin))

# Configuración del sensor PIR
pir_pin = Pin(26, Pin.IN)
# Initialize Wi-Fi connection
station = wifi_init()  # Using Wifi_lib for connection
# Umbrales de temperatura y humedad
umbral_temperatura = 30.0  # Ajusta el valor según tus necesidades
umbral_humedad = 70.0      # Ajusta el valor según tus necesidades
url_backend = ""
url_get_bebe = ""
url_backend_registro_humedad= ""
url_backend_registro_temperatura= ""
url_get_movimiento = ""

# Variable global para almacenar el id del bebé
id_bebe = None
movimiento = False

def obtener_id_bebe():
    global id_bebe
    try:
        response = requests.get(url_get_bebe)
        print("Respuesta ID:", response.text)
        if response.status_code == 200:
            nuevo_id = int(response.text)  # Intenta convertir a entero
            if nuevo_id:  # Solo actualizar si el ID no es nulo o cero
                id_bebe = nuevo_id
                print(f"ID del bebé obtenido: {id_bebe}")
            else:
                print("El ID obtenido no es válido.")
        else:
            print(f"Error al obtener el ID del bebé: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error al realizar la solicitud GET: {e}")


def obtener_estado_movimiento():
    """
    Realiza una solicitud GET para actualizar el estado de la variable global movimiento.
    """
    global movimiento
    try:
        response = requests.get(url_get_movimiento)
        print("Respuesta Movimiento:", response.text)
        if response.status_code == 200:
            # Convertir el texto de la respuesta a un valor booleano
            nuevo_estado = response.text.lower() == "true"
            movimiento = nuevo_estado
            print(f"Estado de movimiento actualizado: {movimiento}")
        else:
            print(f"Error al obtener el estado de movimiento: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error al realizar la solicitud GET: {e}")

        
# Función para registrar datos de temperatura
def registrar_temperatura(temperatura):
    global id_bebe
    print(f"Registrando temperatura. ID actual del bebé: {id_bebe}")
    if id_bebe is None:
        print("El ID del bebé no está definido. Por favor, obtén el ID primero.")
        return

    url = url_backend_registro_temperatura.format(idBebe=id_bebe, temperatura=temperatura)
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print(f"Registro exitoso: Temperatura {temperatura}, ID Bebé {id_bebe}")
        else:
            print(f"Error al registrar los datos: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error al realizar la solicitud POST: {e}")

# Función para registrar datos de humedad
def registrar_humedad(temperatura):
    global id_bebe
    if id_bebe is None:
        print("El ID del bebé no está definido. Por favor, obtén el ID primero.")
        return

    url = url_backend_registro_humedad.format(idBebe=id_bebe, temperatura=temperatura)
    try:
        response = requests.post(url)
        if response.status_code == 200:
            print(f"Registro exitoso: Temperatura {temperatura}, ID Bebé {id_bebe}")
        else:
            print(f"Error al registrar los datos: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error al realizar la solicitud POST: {e}")



def leer_dht22():
    # Leer el sensor y obtener la temperatura y humedad
    dht_sensor.measure()
    temperatura = dht_sensor.temperature()
    humedad = dht_sensor.humidity()
    return temperatura, humedad

def set_angle(angle):
    """Convierte el ángulo (0-180) a un duty cycle y lo envía al servo."""
    duty = int(40 + (angle / 180) * 115)  # Escalar entre 40 y 155 (0.5ms a 2.5ms)
    servo_pin.duty(duty)

def smooth_rotate(start_angle, end_angle, duration):
    """
    Mueve el servo suavemente entre dos ángulos en un tiempo especificado.
    
    Args:
        start_angle (int): Ángulo inicial.
        end_angle (int): Ángulo final.
        duration (int): Tiempo total de transición en milisegundos.
    """
    steps = 120  # Cantidad de pasos para interpolar (más pasos = movimiento más suave)
    step_time = duration // steps  # Tiempo entre pasos (ms)
    step_size = (end_angle - start_angle) / steps  # Tamaño de cada paso

    for i in range(steps + 1):
        current_angle = start_angle + step_size * i
        set_angle(current_angle)
        sleep_ms(step_time)



try:
    print("Girando suavemente...")
    obtener_id_bebe()
    # Variable para controlar el tiempo de registro
    last_record_time = time.time()  # Inicializar con el tiempo actual
    start_mov_time = None  # Tiempo de inicio del movimiento continuo

    while True:
        try:
            if id_bebe is None:
                print("Intentando obtener el ID del bebé...")
                obtener_id_bebe()
            else:
                movimiento_detectado = pir_pin.value()
                current_time = time.time()

                if movimiento_detectado == 1:
                    if start_mov_time is None:
                        start_mov_time = current_time  # Inicia el tiempo de detección continua
                    elif current_time - start_mov_time >= 5:  # Si han pasado 15 segundos
                        print("!!!!!!!!!!!!!!!!!!!!!!")                        
                        print("BEBE EN MOVIMIENTO")
                        print("!!!!!!!!!!!!!!!!!!!!!!") 
                        start_mov_time = None  # Reinicia el tiempo para futuras detecciones
                else:
                    start_mov_time = None  # Si no hay movimiento, reinicia el contador

                temperatura, humedad = leer_dht22()
                print("Temperatura DHT22: {:.2f}°C, Humedad: {:.2f}%".format(temperatura, humedad))
                # Obtener el estado de movimiento
                obtener_estado_movimiento()

                # Verificar el estado de movimiento
                if movimiento:
                    # Rotación suave solo si el movimiento está habilitado
                    smooth_rotate(0, 180, 5000)
                    smooth_rotate(180, 0, 5000)

                # Control del tiempo para registrar datos
                if current_time - last_record_time >= 60:  # 60 segundos
                    # Registrar datos de temperatura y humedad
                    registrar_temperatura(temperatura)
                    registrar_humedad(humedad)

                    # Actualizar el tiempo del último registro
                    last_record_time = current_time
        except OSError as e:
            print("Error al leer el sensor DHT22:", e)
except KeyboardInterrupt:
    print("Detenido por el usuario")
    servo_pin.deinit()
