# Importación de librerías
from utils import project, contenedor_virtual
import time
import paho.mqtt.client as mqtt
import json
import pymysql

# Configuración de mqtt 
clientId = "Contenedor 1"
port = 1883
host = "localhost"
client = mqtt.Client(clientId)
client.connect(host)

# Limites de temperatura y número de hielera
limite_inferior = 2
limite_superior = 8
numero_hielera = 1

# Importando sensores y actuadores del proyecto
main = project()

# Diccionario Python
cliente1 = {
    "N_hielera": numero_hielera,
    "vmin": limite_inferior,
    "vmax" : limite_superior
}

contenedor_virtual_2 = contenedor_virtual(2)
contenedor_virtual_3 = contenedor_virtual(3)

# main.lcd_write('Hola')
# main.led_on('verde')

while True:

    # Lectura del sensor
    humidity, temperature = main.control_temp(2,8)

    # Escritura en la lcd
    main.lcd_write(f"Temp : {temperature} C  \nHumedad : {humidity} %")

    # Envío de información por mqtt
    cliente1["Temperatura"] = temperature
    cliente1["Humedad"] = humidity
    cliente_JSON = json.dumps(cliente1)
    client.publish("TempHum", cliente_JSON)

    cliente_JSON2 = json.dumps(contenedor_virtual_2.lectura())
    client.publish("TempHum", cliente_JSON2)

    cliente_JSON3 = json.dumps(contenedor_virtual_3.lectura())
    client.publish("TempHum", cliente_JSON3)

    #Conexion al localhost de mariadb
    '''db = pymysql.connect(host="localhost", user="root", password="team7mariadb", db="proyecto_equipo7test", charset="utf8mb4")
    try:
        cur = db.cursor()
        while True:
            if temperature is not None and humidity is not None:
                sql = "CALL inserta_dato2(%s,%s,%s);" 
                print(temperature,"C"," ",humidity)
                cur.execute(sql, (numero_hielera, temperature, humidity))
                db.commit()
                time.sleep(30)
                print("todo chido")
            else:
                print("failed to get reading. Try again!")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
                db.close()
                time.sleep(1)'''