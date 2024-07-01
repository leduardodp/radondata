from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pytz
import random , redis , json
from django.core.mail import send_mail
from celery import shared_task

concentracion = 0.0
media = 0.0

#Configuración cliente InfluxDB
client = InfluxDBClient(
        url="http://localhost:8086",
        token="ntbYiWCrZN8xLl-hyZze4zzCZdB28r642Xsommyepwc_H0twV-Ad0wGW5QzvwTT0nH7-EiKx0kXHmMp8JRjqGQ==",
        org="Universidade de Vigo",
        bucket="radon"
    )

#Configuración broker Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

@shared_task(bind=True)
def write_data_every_minute(self):
    bucket="radon"
    write_api = client.write_api(write_options=SYNCHRONOUS)
    #Escribir datos en influx
    print("Ejemplo de escritura de datos en InfluxDB")
    data = []
    for aula in range(1): 
        p = Point("my_measurement").tag("Aula", str(aula)).field("concentracion", random.uniform(0, 300))
        data.append(p)
        write_api.write(bucket=bucket, org=client.org, record=p)

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@shared_task(bind=True)
def read_data_every_minute(self):
    global concentracion

    #Leer datos de influx
    print("Ejemplo de lectura de datos en InfluxDB")
    query_api = client.query_api()

    # Definir la consulta
    query =  """from(bucket:"radon") |> range(start: -2h) |> filter(fn: (r) => r._measurement ==   "my_measurement")"""
    # Ejecutar la consulta
    results = query_api.query(org=client.org, query=query)

    #Crear una lista para almacenar los datos
    data = []
    for result in results:
        for record in result.records:
            concentracion = round(record.get_value(),2)
            #Añadir los datos a la lista

            # Convertir el timestamp a hora local
            timestamp_utc = record.get_time()
            timezone_local = pytz.timezone('Europe/Madrid')  # Ajusta a tu zona horaria local
            timestamp_local = timestamp_utc.astimezone(timezone_local).isoformat()
            data.append({
                "x": timestamp_local, 
                "y":concentracion
                })
            #Imprimir los datos
            print("Aula:", record.values.get("Aula"),\
                "Concentracion :",concentracion,"Bq/m3")
    #Devolver los datos en formato JSON
    return json.dumps(data)
    
#Media Diaria
@shared_task(bind=True)
def read_media_data_every_minute(self):
    global media
    query_api = client.query_api()
    # Definir la consulta
    query =  """ from(bucket:"radon") |> range(start: -1d) |> filter(fn: (r) => r._measurement == "my_measurement") |> mean() """
    # Ejecutar la consulta
    results = query_api.query(org=client.org, query=query)
    for result in results:
        for record in result.records:
            media = round(record.get_value(),2)
            print("Aula:", record.values.get("Aula"), \
                "Concentracion media: ", media)
            redis_client.set('media', media)
            return media
        
#Media Semanal
@shared_task(bind=True)
def read_media_data_every_minute(self):
    global media
    query_api = client.query_api()
    # Definir la consulta
    query =  """ from(bucket:"radon") |> range(start: -7d) |> filter(fn: (r) => r._measurement == "my_measurement") |> mean() """
    # Ejecutar la consulta
    results = query_api.query(org=client.org, query=query)
    for result in results:
        for record in result.records:
            media = round(record.get_value(),2)
            print("Aula:", record.values.get("Aula"), \
                "Concentracion media: ", media)
            redis_client.set('media', media)
            return media

#Media Mensual
@shared_task(bind=True)
def read_media_data_every_minute(self):
    global media
    query_api = client.query_api()
    # Definir la consulta
    query =  """ from(bucket:"radon") |> range(start:-30d) |> filter(fn: (r) => r._measurement == "my_measurement") |> mean() """
    # Ejecutar la consulta
    results = query_api.query(org=client.org, query=query)
    for result in results:
        for record in result.records:
            media = round(record.get_value(),2)
            print("Aula:", record.values.get("Aula"), \
                "Concentracion media: ", media)
            redis_client.set('media', media)
            return media

def media_funcion():
    return float(redis_client.get('media').decode('utf-8')) if redis_client.get('media') else 0.0

def concentracion_funcion():
    return float(redis_client.get('concentracion').decode('utf-8')) if redis_client.get('concentracion') else 0.0