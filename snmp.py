import json
from easysnmp import Session
from flask import Flask
from flask_restful import Resource, Api
import random
from time import sleep

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


class Tripplite_Smart:
    def __init__(self, ip):
        self.ip = ip
        session = Session(hostname=self.ip, community='public', version=1)

        # values discovered by manually inspecting
        #  `snmpwalk -v 1 -c public 10.0.0.143`
        # the leading 'iso.' is replaced with '.1.' because... science?

        # SMART500RT1U is a 300 watt device, raw value appears to be x/1000
        load_raw = session.get('.1.3.6.1.2.1.33.1.4.4.1.5.1')
        self.load = int(float(load_raw.value) * 0.3)

        uptime_raw = session.get('.1.3.6.1.2.1.1.3.0')
        self.uptime_days = int(float(uptime_raw.value) / 8640000)

        self.ac_voltage = int(session.get('.1.3.6.1.2.1.33.1.3.3.1.3.1').value)
        self.battery_temp = int(session.get('.1.3.6.1.2.1.33.1.2.7.0').value)
        mac = str(session.get('.1.3.6.1.2.1.2.2.1.6.2').value)
        self.mac = toRaw(mac).hex().upper()
        self.model = session.get('.1.3.6.1.2.1.33.1.1.2.0').value


def toRaw(s):
    # https://stackoverflow.com/a/70082688
    x = [ord(i) for i in list(s)]
    return bytearray(x)


class battery(Resource):
    def __init__(self, **kwargs):
        self.os = kwargs['os']

    def get(self):
        ups = Tripplite_Smart(self.os.getenv('SNMP_ADDRESS'))
        return(ups.__dict__)


def flask(os):
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(battery, '/power/', resource_class_kwargs={'os': os})
    app.run(host='0.0.0.0', port='5000')


def influx_reporter(os, update_interval):
    '''
    report metrics to influxdb
    '''
    bucket = os.getenv('INFLUX_BUCKET')
    org = os.getenv('INFLUX_ORG')
    token = os.getenv('INFLUX_TOKEN')
    url = os.getenv('INFLUX_URL')

    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org)

    write_api = client.write_api(write_options=SYNCHRONOUS)
    ups_ip = os.getenv('SNMP_ADDRESS')

    while True:
        sleep(random.randrange(1, update_interval))
        ups = Tripplite_Smart(ups_ip)

        load = influxdb_client.Point("power").tag("mac", ups.mac).field("load", ups.load)
        battery_temp = influxdb_client.Point("power").tag("mac", ups.mac).field("battery_temp", ups.battery_temp)
        ac_voltage = influxdb_client.Point("power").tag("mac", ups.mac).field("ac_voltage", ups.ac_voltage)

        write_api.write(bucket=bucket, org=org, record=load)
        write_api.write(bucket=bucket, org=org, record=battery_temp)
        write_api.write(bucket=bucket, org=org, record=ac_voltage)


if __name__ == '__main__':
    def main():
        import os
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument('--flask', action='store_true')
        parser.add_argument('--influx', action='store_true')
        parser.add_argument('--interval', type=int, default=120)
        args = parser.parse_args()

        if args.flask:
            flask(os)
        elif args.influx:
            influx_reporter(os, args.interval)
        else:
            ups = Tripplite_Smart(os.getenv('SNMP_ADDRESS'))
            print(json.dumps(ups.__dict__))

    main()
