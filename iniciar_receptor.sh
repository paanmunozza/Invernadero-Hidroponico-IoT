#!/bin/bash

# Acceder al directorio del proyecto
cd /home/USUARIO/hidroponico

# Ejecutar el receptor MQTT
exec /home/USUARIO/hidroponico/venv/bin/python receptor.py
