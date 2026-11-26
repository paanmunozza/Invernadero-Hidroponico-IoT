#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// ---------- Pines ----------
#define DHTPIN 15
#define DHTTYPE DHT22
#define TRIG_PIN 19
#define ECHO_PIN 22
#define SOIL_PIN 34
#define ONEWIRE_PIN 4

// ---------- Red y broker ----------
const char* WIFI_SSID = "NOMBRE_DE_RED";
const char* WIFI_PASS = "CONTRASENA_WIFI";
const char* mqtt_server = "IP_DEL_BROKER";
const char* TEMA = "hidroponico/lecturas";

// Intervalo entre lecturas: 1 minuto
const unsigned long INTERVALO = 60000;
unsigned long ultimoEnvio = 0;

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(ONEWIRE_PIN);
DallasTemperature sensorAgua(&oneWire);

float medirDistanciaCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duracion = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duracion == 0) return NAN;
  return duracion * 0.0343 / 2;
}

float medirTempAgua() {
  sensorAgua.requestTemperatures();
  float t = sensorAgua.getTempCByIndex(0);
  if (t == DEVICE_DISCONNECTED_C) return NAN;
  return t;
}

String num(float valor) {
  if (isnan(valor)) return "null";
  return String(valor, 1);
}

void conectarWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado");
}

void conectarBroker() {
  while (!client.connected()) {
    Serial.print("Conectando al broker...");
    if (client.connect("esp32-hidroponico")) {
      Serial.println("listo");
    } else {
      Serial.print("fallo, codigo: ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  sensorAgua.begin();
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(SOIL_PIN, INPUT);

  conectarWiFi();
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) conectarWiFi();
  if (!client.connected()) conectarBroker();
  client.loop();

  if (millis() - ultimoEnvio >= INTERVALO || ultimoEnvio == 0) {
    ultimoEnvio = millis();

    float tempAmb = dht.readTemperature();
    float humAmb = dht.readHumidity();
    float tempAgua = medirTempAgua();
    float distancia = medirDistanciaCm();
    int suelo = analogRead(SOIL_PIN);

    String json = "{\"dispositivo\":\"esp32-1\"";
    json += ",\"temp_ambiente\":" + num(tempAmb);
    json += ",\"humedad_ambiente\":" + num(humAmb);
    json += ",\"temp_agua\":" + num(tempAgua);
    json += ",\"humedad_suelo\":" + String(suelo);
    json += ",\"nivel_crecimiento\":" + num(distancia);
    json += "}";

    client.publish(TEMA, json.c_str());
    Serial.println(json);
  }
}
