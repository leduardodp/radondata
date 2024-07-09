from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pytz
import random , redis , json
from django.core.mail import send_mail
from celery import shared_task
from apps.aulas.models import Aula


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
    aulas = Aula.objects.all()
    for aula in aulas: 
        p = Point("my_measurement").tag("name",str(aula)).field("concentracion", random.uniform(0, 300))
        write_api.write(bucket=bucket, org=client.org, record=p)
    



@shared_task(bind=True)
def read_daily_data(self):
    global concentracion

    #Leer datos de influx
    print("Ejemplo de lectura de datos en InfluxDB")
    query_api = client.query_api()

    # Definir la consulta
    query =  """from(bucket:"radon")    
                |> range(start: -24h) 
                |> filter(fn: (r) => r._measurement ==   "my_measurement")"""
    # Ejecutar la consulta
    results = query_api.query(org=client.org, query=query)

    #Crear una lista para almacenar los datos
    #data = []
    #Crear un diccionario para almacenar los datos por aula
    for result in results:
        aula_data =[]
        for record in result.records:
            name = record.values.get("name")
            concentracion = round(record.get_value(),2)
            # Convertir el timestamp a hora local
            timestamp_utc = record.get_time()
            timezone_local = pytz.timezone('Europe/Madrid')  # Ajusta a tu zona horaria local
            timestamp_local = timestamp_utc.astimezone(timezone_local).isoformat()

            # Agregar los datos a la lista correspondiente a la aula
            aula_data.append({
                "x": timestamp_local, 
                "y": concentracion
                })
        
        redis_client.set(f'daily_data_{name}', json.dumps(aula_data))
    
#Media Diaria
@shared_task(bind=True)
def read_daily_media_data(self):
    query_api = client.query_api()
    # Definir la consulta
    query =  """ 
        import "date"
        start_day = date.truncate(t: now(), unit: 1d)
        from(bucket:"radon")   
            |> range(start: start_day, stop: now()) 
            |> filter(fn: (r) => r._measurement == "my_measurement") 
            |> mean() 
            """
    # Ejecutar la consulta
    results = query_api.query(org=client.org, query=query)
    for result in results:
        for record in result.records:
            name = record.values.get("name")
            media = round(record.get_value(),2)
            print(f"Media diaria de {name}: {media}")
            redis_client.set(f'daily_media_{name}', media)

#Media semanal
@shared_task(bind=True)
def read_weekly_media_data(self):
    query_api = client.query_api()
    # Definir la consulta
    query =  """
        import "date"
        start_week = date.truncate(t: now(), unit: 1w)
        from(bucket: "radon")
            |> range(start: start_week, stop: now())
            |> filter(fn: (r) => r._measurement == "my_measurement")
            |> mean()
            """

    # Ejecutar la consulta
    results = query_api.query(org=client.org, query=query)
    for result in results:
        for record in result.records: 
            name = record.values.get("name")
            media = round(record.get_value(),2)
            print(f"Media semanal de {name}: {media}")
            redis_client.set(f'weekly_media_{name}', media)

#Media mensual
@shared_task(bind=True)
def read_monthly_media_data(self):
    query_api = client.query_api()
    # Definir la consulta
    query =  """ 
        import "date"
        start_month = date.truncate(t: now(), unit: 1mo)
        from(bucket: "radon")
            |> range(start: start_month, stop: now())
            |> filter(fn: (r) => r._measurement == "my_measurement")
            |> mean()
            """

    # Ejecutar la consulta
    results = query_api.query(org=client.org, query=query)
    for result in results:
        for record in result.records:
            name = record.values.get("name")
            media = round(record.get_value(),2)
            print(f"Media mensual de {name}: {media}")
            redis_client.set(f'monthly_media_{name}', media)

def get_media_diaria(name):
    media = redis_client.get(f'daily_media_{name}')
    return float(media.decode('utf-8')) if media else 0.0

def get_media_semanal(name):
    media = redis_client.get(f'weekly_media_{name}')
    return float(media.decode('utf-8')) if media else 0.0

def get_media_mensual(name):
    media = redis_client.get(f'monthly_media_{name}')
    return float(media.decode('utf-8')) if media else 0.0

def get_json(name):
    datos = redis_client.get(f'daily_data_{name}')
    return json.loads(datos.decode('utf-8')) if datos else []


def concentracion_funcion():
    return float(redis_client.get('concentracion').decode('utf-8')) if redis_client.get('concentracion') else 0.0