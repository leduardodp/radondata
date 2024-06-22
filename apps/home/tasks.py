from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random , redis
from django.core.mail import send_mail
from celery import shared_task

concentracion = 0.0
media = 0.0

client = InfluxDBClient(
        url="http://localhost:8086",
        token="ntbYiWCrZN8xLl-hyZze4zzCZdB28r642Xsommyepwc_H0twV-Ad0wGW5QzvwTT0nH7-EiKx0kXHmMp8JRjqGQ==",
        org="Universidade de Vigo",
        bucket="radon"
    )

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

@shared_task(bind=True)
def read_data_every_minute(self):
    global concentracion
    #Leer datos de influx
    print("Ejemplo de lectura de datos en InfluxDB")
    query_api = client.query_api()
    # Definir la consulta
    query =  """from(bucket:"radon") |> range(start: -10m) |> filter(fn: (r) => r._measurement ==   "my_measurement")"""
    # Ejecutar la consulta
    results = query_api.query(org=client.org, query=query)
    #data = []
    for result in results:
        for record in result.records:
            concentracion = round(record.get_value(),2)
            #data.append({"_time": record.get_time(),"_value":concentracion})
            print("Aula:", record.values.get("Aula"),\
                "Concentracion :",concentracion,"Bq/m3")
            redis_client.set('concentracion', concentracion)

@shared_task(bind=True)
def read_media_data_every_minute(self):
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
                "Concentracion media: ",round(record.get_value(),2))
            redis_client.set('media', media)



def media_funcion():
    return float(redis_client.get('media').decode('utf-8')) if redis_client.get('media') else 0.0

def concentracion_funcion():
    return float(redis_client.get('concentracion').decode('utf-8')) if redis_client.get('concentracion') else 0.0