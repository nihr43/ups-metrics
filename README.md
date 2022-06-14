# ups-metrics

Endpoint for collecting metrics on Tripplite SMART series ups devices.

This primarily exists so that I dont have to deal with SNMP or this thing's poor web ui anymore; checking wattage is now just a quick glance at some json.

I do not know if the embedded resource ids (OIDs? MIBs?) are consistent across devices.

## misc

find a tripplite SMART device on our broadcast domain:

```
sudo arp -n | grep '00:40:9d'
```

dump all snmp data from a device:

```
snmpwalk -v 1 -c public 10.0.0.143
```

Required OS packages for building python packages:

```
libsnmp-dev
```
