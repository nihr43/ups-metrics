import os

from easysnmp import Session

session = Session(hostname=os.environ.get('SNMP_ADDRESS'), community='public',
                  version=1)

load = session.get('.1.3.6.1.2.1.33.1.4.4.1.5.1')
ac_voltage = session.get('.1.3.6.1.2.1.33.1.3.3.1.3.1')
battery_temp = session.get('.1.3.6.1.2.1.33.1.2.7.0')

# 300 watt device
wattage = int(float(load.value)*0.3)

env = os.environ.copy()
if env.get("DEBUG", False) == "True":
    print('wattage = ' + str(wattage))
    print('ac_voltage = ' + str(ac_voltage.value))
    print('battery_temp = ' + str(battery_temp.value))
