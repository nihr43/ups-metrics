from easysnmp import Session
from flask import Flask
from flask_restful import Resource, Api


class Tripplite_Smart:
    def __init__(self, ip):
        self.ip = ip
        session = Session(hostname=self.ip, community='public', version=1)

        # values discovered by manually inspecting
        #  `snmpwalk -v 1 -c public 10.0.0.143`
        # the leading 'iso.' is replaced with '.1.' because... science?

        # SMART500RT1U is a 300 watt device, raw value appears to be x/1000
        load_raw = session.get('.1.3.6.1.2.1.33.1.4.4.1.5.1')
        self.load = int(float(load_raw.value)*0.3)

        uptime_raw = session.get('.1.3.6.1.2.1.1.3.0')
        self.uptime_days = int(float(uptime_raw.value)/8640000)

        self.ac_voltage = int(session.get('.1.3.6.1.2.1.33.1.3.3.1.3.1').value)
        self.battery_temp = int(session.get('.1.3.6.1.2.1.33.1.2.7.0').value)
        self.mac = session.get('.1.3.6.1.2.1.2.2.1.6.2').value
        self.model = session.get('.1.3.6.1.2.1.33.1.1.2.0').value


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


if __name__ == '__main__':
    def main():
        import os
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument('--flask', action='store_true')
        args = parser.parse_args()

        if args.flask:
            flask(os)

    main()
