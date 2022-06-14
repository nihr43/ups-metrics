import os

from easysnmp import Session
from flask import Flask
from flask import jsonify
from flask_restful import Resource, Api


class battery(Resource):
    def get(self):
        session = Session(hostname=os.environ.get('SNMP_ADDRESS'),
                          community='public', version=1)

        # values discovered by manually inspecting
        #  `snmpwalk -v 1 -c public 10.0.0.143`
        # here the leading 'iso.' is replaced with '.1.' because... science?
        load_raw = session.get('.1.3.6.1.2.1.33.1.4.4.1.5.1')
        # this is a 300 watt device, raw value appears to be x/1000
        load = int(float(load_raw.value)*0.3)
        ac_voltage = session.get('.1.3.6.1.2.1.33.1.3.3.1.3.1')
        battery_temp = session.get('.1.3.6.1.2.1.33.1.2.7.0')
        mac = session.get('.1.3.6.1.2.1.2.2.1.6.2')
        uptime_raw = session.get('.1.3.6.1.2.1.1.3.0')
        uptime_days = int(float(uptime_raw.value)/8640000)
        model = session.get('.1.3.6.1.2.1.33.1.1.2.0')

        vals = []
        vals.append({'load': load,
                     'ac_voltage': ac_voltage.value,
                     'battery_temp': battery_temp.value,
                     'uptime_days': uptime_days,
                     'model': model.value})

        return(jsonify(ups=vals))


def main():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(battery, '/power/')
    app.run(host='0.0.0.0', port='5000')


if __name__ == '__main__':
    main()
