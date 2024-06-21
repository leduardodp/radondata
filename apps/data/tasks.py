# myapp/tasks.py
from celery import shared_task
import sqlite3
from django.core.mail import send_mail
#from .read_data import get_users ,media_funcion

#Tarea de prueba
@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Done"


#Tarea para enviar emails
def get_users():
    # Conecta a la base de datos SQLite
    conn = sqlite3.connect('db.sqlite3')

    # Obtén la lista de usuarios
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM authentication_customuser')
    users = cursor.fetchall()

    # Cierra la conexión a la base de datos
    conn.close()

    # Devuelve la lista de usuarios
    return [user[0] for user in users]

@shared_task(bind=True)
def send_mail_func(self):
    users = get_users()
    for user in users:
        subject = 'Concentración media de radón'
        message = f'Aquí están los datos de concentracion media en los ultimos 10 min: \n\n Bq/m3'
        email_from = 'ldagostino@alumnos.uvigo.es'
        send_mail(subject, message, email_from, [user])
    return "Sent"














'''from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random

# Configuración de la conexión a InfluxDB
client = InfluxDBClient(
    url="http://localhost:8086",
    token="ntbYiWCrZN8xLl-hyZze4zzCZdB28r642Xsommyepwc_H0twV-Ad0wGW5QzvwTT0nH7-EiKx0kXHmMp8JRjqGQ==",
    org="Universidade de Vigo",
    bucket="radon"
)
write_api = client.write_api(write_options=SYNCHRONOUS)

concentracion = 0.0
media = 0.0

@shared_task
def write_data_24h_task():
    global concentracion
    #Escribir datos en influx
    print("Ejemplo de escritura de datos en InfluxDB")
    data = []
    for aula in range(1): 
        p = Point("my_measurement").tag("Aula", str(aula)).field("concentracion", random.uniform(0, 300))
        data.append(p)
        write_api.write(bucket="radon", org="Universidade de Vigo", record=p)
    return data

@shared_task
def read_data_1m_task():
    global concentracion
    #Leer datos de influx
    print("Ejemplo de lectura de datos en InfluxDB")
    query_api = client.query_api()
    # Definir la consulta
    query =  """from(bucket:"radon") |> range(start: -10m) |> filter(fn: (r) => r._measurement ==   "my_measurement")"""
    # Ejecutar la consulta
    results = query_api.query(org="Universidade de Vigo", query=query)
    data = []
    for result in results:
        for record in result.records:
            concentracion = round(record.get_value(),2)
            data.append({"_time": record.get_time(),"_value":concentracion})
            print("Aula:", record.values.get("Aula"),\
                "Concentracion :",concentracion,"Bq/m3")
    return data

@shared_task
def read_media_1m_task():
    global media
    query_api = client.query_api()
    # Definir la consulta
    query =  """ from(bucket:"radon") |> range(start: -10m) |> filter(fn: (r) => r._measurement == "my_measurement") |> mean() """
    # Ejecutar la consulta
    results = query_api.query(org=client.org, query=query)
    for result in results:
        for record in result.records:
            media = round(record.get_value(),2)
            print("Aula:", record.values.get("Aula"), \
                "Concentracion media: ", media )
    return media'''



