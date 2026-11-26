CREATE DATABASE IF NOT EXISTS hidroponia;
USE hidroponia;

-- Tabla de mediciones de los sensores

CREATE TABLE IF NOT EXISTS lecturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dispositivo VARCHAR(50),
    temp_ambiente FLOAT,
    temp_agua FLOAT,
    humedad_ambiente FLOAT,
    humedad_suelo FLOAT,
    nivel_crecimiento FLOAT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Creacion del usuario y asignacion de permisos

CREATE USER IF NOT EXISTS 'hidro'@'localhost'
IDENTIFIED BY 'TU_CLAVE';

GRANT SELECT, INSERT ON hidroponia.*
TO 'hidro'@'localhost';

FLUSH PRIVILEGES;
