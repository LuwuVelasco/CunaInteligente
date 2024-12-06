# Cuna Inteligente - Código IoT (Thonny y MicroPython)

Este repositorio contiene los scripts en MicroPython utilizados para controlar los dispositivos IoT del proyecto **Cuna Inteligente**. Los scripts se ejecutan en un microcontrolador ESP32 y son responsables de capturar datos de los sensores, procesarlos y enviarlos al backend.

## Contexto del Desarrollo

El desarrollo de los scripts en Thonny fue una parte fundamental del proyecto, ya que marcó el progreso continuo a lo largo de la materia. Cada parcial estuvo enfocado en lograr avances significativos en la programación y configuración de los dispositivos IoT, consolidando el aprendizaje y sentando las bases para la solución final presentada en este repositorio. Estos avances permitieron:

- Integrar sensores y actuadores de manera eficiente.
- Implementar comunicación en tiempo real con el backend.
- Desarrollar un manejo robusto de errores y reconexión.

## Problemática

El monitoreo constante de las condiciones del bebé, como temperatura, humedad, movimiento y sonidos, requiere una solución eficiente y de bajo costo. El ESP32, programado con MicroPython, permite gestionar múltiples sensores y enviar datos en tiempo real al servidor para su análisis.

## Objetivos del Código IoT

- Capturar datos de sensores conectados al ESP32 (DHT22, PIR, micrófono).
- Enviar datos al backend mediante solicitudes HTTP.
- Recibir comandos del servidor para controlar dispositivos como el servomotor y el reproductor de audio (DFPlayer Mini).
- Implementar un manejo eficiente de errores y reconexión en caso de fallos en la comunicación.

## Sensores y Actuadores Utilizados

1. **DHT22**: Sensor de temperatura y humedad.
2. **PIR**: Sensor de movimiento.
3. **Micrófono**: Captura el llanto del bebé.
4. **Servomotor**: Permite el movimiento controlado de la cuna.
5. **DFPlayer Mini**: Reproduce sonidos o canciones para el bebé.

## Requisitos del Sistema

- **Microcontrolador**: ESP32
- **IDE**: [Thonny](https://thonny.org/) con soporte para MicroPython.
- **Bibliotecas**: `urequests`, `machine`, `time`, `dht`, entre otras.

## Instalación y Configuración

1. **Configurar el ESP32**:  
   Instalar MicroPython en el ESP32 siguiendo las instrucciones de la documentación oficial.
