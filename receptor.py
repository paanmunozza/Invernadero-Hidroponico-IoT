import json
import os
from datetime import datetime

import gspread
import paho.mqtt.client as mqtt
import pymysql
from dotenv import load_dotenv

load_dotenv()

# ---------- Configuracion MQTT ----------
BROKER = os.getenv("MQTT_BROKER", "127.0.0.1")
PUERTO = int(os.getenv("MQTT_PORT", "1883"))
TEMA = os.getenv("MQTT_TOPIC", "hidroponico/lecturas")

# ---------- Configuracion MariaDB ----------
DB = dict(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "hidro"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME", "hidroponia"),
)

# ---------- Configuracion Google Sheets ----------
CREDENCIALES = os.getenv("GOOGLE_CREDENTIALS", "credenciales.json")
NOMBRE_HOJA = os.getenv("SHEET_NAME", "Hidroponica_datos")

# Dispositivos de simulacion
SIMULADOS = ("esp32-simulado", "simulado")

CAMPOS = [
    "dispositivo",
    "temp_ambiente",
    "temp_agua",
    "humedad_ambiente",
    "humedad_suelo",
    "nivel_crecimiento",
]

# ---------- Conexion a Google Sheets ----------
gc = gspread.service_account(filename=CREDENCIALES)
hoja = gc.open(NOMBRE_HOJA).sheet1


# ---------- Almacenamiento en MariaDB ----------
def guardar_db(datos):
    valores = [datos.get(campo) for campo in CAMPOS]
    columnas = ", ".join(CAMPOS)
    marcas = ", ".join(["%s"] * len(CAMPOS))
    sql = f"INSERT INTO lecturas ({columnas}) VALUES ({marcas})"

    conexion = pymysql.connect(**DB)
    try:
        with conexion.cursor() as cursor:
            cursor.execute(sql, valores)
        conexion.commit()
    finally:
        conexion.close()


# ---------- Envio a Google Sheets ----------
def enviar_drive(datos):
    if datos.get("dispositivo") in SIMULADOS:
        return False

    fila = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    fila += [datos.get(campo) for campo in CAMPOS]

    hoja.append_row(fila, value_input_option="USER_ENTERED")
    return True


# ---------- Conexion al broker MQTT ----------
def al_conectar(client, userdata, flags, reason_code, properties):
    print("Conectado al broker, codigo:", reason_code, flush=True)
    client.subscribe(TEMA)


# ---------- Recepcion de mediciones ----------
def al_recibir(client, userdata, msg):
    try:
        datos = json.loads(msg.payload.decode())
    except Exception as error:
        print("Mensaje invalido:", error, flush=True)
        return

    try:
        guardar_db(datos)
        print("Guardado en MariaDB:", datos, flush=True)
    except Exception as error:
        print("Error en MariaDB:", error, flush=True)

    try:
        if enviar_drive(datos):
            print("Enviado a Drive", flush=True)
        else:
            print("Simulado: no se envia a Drive", flush=True)
    except Exception as error:
        print("Error en Drive:", error, flush=True)


# ---------- Inicializacion del cliente MQTT ----------
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = al_conectar
client.on_message = al_recibir

client.connect(BROKER, PUERTO)
client.loop_forever()
