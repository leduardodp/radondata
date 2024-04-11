from django.conf import settings
from influxdb import InfluxDBClient

def get_influxdb_client():
    client = InfluxDBClient(
        settings.INFLUXDB_HOST,
        settings.INFLUXDB_PORT,
        settings.INFLUXDB_USERNAME,
        settings.INFLUXDB_PASSWORD,
        settings.INFLUXDB_DATABASE
    )
    return client
