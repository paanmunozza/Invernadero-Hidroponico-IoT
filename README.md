# Invernadero hidropónico IoT

## Descripción del proyecto

Sistema IoT diseñado para el monitoreo de un cultivo hidropónico de lechuga orejona, mediante sensores conectados a una ESP32, comunicación MQTT, almacenamiento en MariaDB e integración con Google Sheets.

## Objetivo

Monitorear las condiciones ambientales y las variables relacionadas con el desarrollo de la lechuga orejona, facilitando el registro y análisis de las mediciones.

## Componentes utilizados

| Componente | Función |
|---|---|
| ESP32 | Adquisición y transmisión de datos |
| DHT22 | Temperatura y humedad ambiental |
| DS18B20 | Temperatura del agua |
| HC-SR04 | Seguimiento del crecimiento vegetal mediante distancia |
| Sensor de humedad | Humedad del sustrato |

## Funcionamiento

1. Los sensores realizan las mediciones correspondientes.
2. La ESP32 procesa las lecturas cada minuto.
3. Los datos se transmiten mediante WiFi y MQTT en formato JSON.
4. Un programa desarrollado en Python recibe las mediciones.
5. Los datos se almacenan en MariaDB.
6. La integración con Google Sheets está diseñada para registrar las mediciones en la nube.

## Tecnologías utilizadas

- ESP32
- Arduino IDE
- Ubuntu
- Mosquitto MQTT
- Python
- MariaDB
- Google Sheets
- Systemd

## Archivos del repositorio

| Archivo | Descripción |
|---|---|
| Invernadero_Hidroponico.ino | Programa principal de la ESP32 |
| Base_de_datos.sql | Estructura de la base de datos |
| receptor.py | Recepción y almacenamiento de mediciones |
| iniciar_receptor.sh | Script de arranque del receptor |
| receptor-hidroponico.service | Servicio automático de Ubuntu |
| requirements.txt | Dependencias de Python |
| .env.example | Plantilla de configuración |
| .gitignore | Exclusión de archivos privados |

## Configuración de red

Durante el desarrollo del proyecto se utilizaron direcciones IP, direcciones MAC y usuarios asignados al equipo de trabajo para identificar los dispositivos ESP32 y Ubuntu dentro de la infraestructura de red de la asignatura IIoT.

La configuración publicada debe adaptarse a la red y al equipo donde se implemente el sistema.

## Seguridad y privacidad

Las contraseñas y claves privadas deben mantenerse fuera del repositorio. Se proporciona una plantilla de configuración con valores genéricos.

Los archivos publicados tienen fines académicos y de documentación.

## Estado del proyecto

El sistema se encuentra completamente implementado y en funcionamiento. Se verificó la adquisición de datos mediante los sensores conectados a la ESP32, la transmisión mediante MQTT, el procesamiento en Python, el almacenamiento en MariaDB y el registro automático en Google Sheets.

El repositorio contiene los códigos y archivos de configuración utilizados para el desarrollo e implementación del proyecto final de la asignatura IIoT.

## Asignatura

Internet Industrial de las Cosas (IIoT).

Ingeniería Mecatrónica.

Alumnos: Devany Sandoval y Paolo Muñoz
