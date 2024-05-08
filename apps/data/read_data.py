from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random , schedule , time , threading

concentracion = 0.0
media = 0.0

def clientInflux():
        # Configuración de la conexión a InfluxDB
    bucket = "radon"
    org = "Universidade de Vigo"
    token = "_kl1c-aCdvw7szgGtvufL_B1JhlT_jnXXxBOqo-jLvC_oAJbiFVOVI3-ipyMkfFqG0FXxZgzvXTLpXo1JhLUqA=="
    url="http://localhost:8086"

    # Creación de cliente en InfluxDB
    client = InfluxDBClient(
        url=url,
        token=token,
        org=org,
        bucket=bucket
    )
    return client


#Funcion para generar datos aleatorios cada minuto
def write_data_24h():
    client = clientInflux()
    bucket = "radon"
    write_api = client.write_api(write_options=SYNCHRONOUS)

    #Escribir datos en influx
    print("Ejemplo de escritura de datos en InfluxDB")
    data = []
    for aula in range(1): 
        p = Point("my_measurement").tag("Aula", str(aula)).field("concentracion", random.uniform(0, 300))
        data.append(p)
        write_api.write(bucket=bucket, org=client.org, record=p)


#Funciones para leer los datos actuales a cada minuto
def read_data_1m():
    global concentracion
    client = clientInflux()
    #Leer datos de influx
    print("Ejemplo de lectura de datos en InfluxDB")
    query_api = client.query_api()
    # Definir la consulta
    query =  """from(bucket:"radon") |> range(start: -10m) |> filter(fn: (r) => r._measurement == "my_measurement")"""
    # Ejecutar la consulta
    results = query_api.query(org=client.org, query=query)
    
    for result in results:
        for record in result.records:
            concentracion = round(record.get_value(),2)
            print("Aula:", record.values.get("Aula"),\
                "Concentracion :",round(record.get_value(),2))
            
def concentracion_funcion():
    return concentracion

def read_media_1m():
    global media
    client = clientInflux()
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
    

def media_funcion():
    return media

def data_task():
    
    schedule.every(30).seconds.do(write_data_24h)
    schedule.every(30).seconds.do(read_data_1m) # Programar la tarea para que se ejecute cada 30 segundos
    schedule.every(30).seconds.do(read_media_1m) 

    while True: # Ejecutar la planificación en un bucle infinito
        schedule.run_pending()
        time.sleep(1)  # Dormir un segundo para evitar uso excesivo de CPU

def async_task():

    t = threading.Thread(target=data_task)   # Crear un hilo para ejecutar las tareas periódicas 

    t.daemon = True  # Hacer que el hilo sea un hilo de fondo, para que se detenga cuando se detenga el programa principal

    t.start()    # Iniciar el hilo