from __future__ import print_function
import argparse, datetime , random, time
from influxdb import InfluxDBClient

USER = 'root'
PASSWORD = 'root'
DBNAME = 'tutorial'

def main(host='localhost', port=8086, nb_day=15):
    """Instanciar conexion al backend."""
    nb_day = 1  # Numero de dias para generar tseries
    timeinterval_min = 10  # Crea un evento cada x minutos
    total_minutes = 1440 * nb_day
    total_records = int(total_minutes / timeinterval_min)
    now = datetime.datetime.today()
    metric = "server_data.cpu_idle"
    series = []

    for i in range(0, total_records):
        past_date = datetime.datetime.now() - datetime.timedelta(minutes=10)
        past_seconds = past_date.timestamp()
        value = random.randint(0, 300)
        hostName = "server-%d" % random.randint(1, 5)
        # pointValues = [int(past_date.strftime('%s')), value, hostName]
        pointValues = {
            "time": int(past_seconds),
            "measurement": metric,
            "fields": {
                "value": value,
            },
            "tags": {
                "hostName": hostName,
            },
        }
        series.append(pointValues)

    print(series)

    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)

    print("Create database: " + DBNAME)
    try:
        client.create_database(DBNAME)
    except InfluxDBClientError:
        # Drop and create
        client.drop_database(DBNAME)
        client.create_database(DBNAME)

    print("Create a retention policy")
    retention_policy = 'server_data'
    client.create_retention_policy(retention_policy, '3d', 3, default=True)

    print("Write points #: {0}".format(total_records))
    client.write_points(series, retention_policy=retention_policy)

    time.sleep(2)

    query = "SELECT MEAN(value) FROM {} WHERE \
            time > now() - 1d GROUP BY time(10m)".format(metric)
    result = client.query(query, database=DBNAME)
    print(result)
    print("Result: {0}".format(result))

    print("Drop database: {}".format(DBNAME))
    client.drop_database(DBNAME)


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname influxdb http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port influxdb http API')
    parser.add_argument('--nb_day', type=int, required=False, default=15,
                        help='number of days to generate time series data')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port, nb_day=args.nb_day)