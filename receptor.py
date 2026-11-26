import json
import paho.mqtt.client as mqtt
import pymysql

# Configuracion del broker MQTT
BROKER = "127.0.0.1"
PUERTO = 1883
TEMA = "hidroponico/lecturas"

# Configuracion de MariaDB
DB = dict(
    host="localhost",
    user="hidro",
    password="TU_CLAVE",
    database="hidroponia",
)

CAMPOS = [
    "dispositivo",
    "temp_ambiente",
    "temp_agua",
    "humedad_ambiente",
    "humedad_suelo",
    "nivel_crecimiento",
]

# Almacenamiento de mediciones
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

# Conexion con el broker MQTT
def al_conectar(client, userdata, flags, reason_code, properties):
    print("Conectado al broker, codigo:", reason_code, flush=True)
    client.subscribe(TEMA)

# Recepcion de mediciones del ESP32
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

# Inicializacion del cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = al_conectar
client.on_message = al_recibir

client.connect(BROKER, PUERTO)
client.loop_forever()
