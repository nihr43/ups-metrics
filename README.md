# ups-metrics

Collect metrics on Tripplite SMART series UPS devices and push to InfluxDB, serve on http, or print to console.

I do not know if the embedded resource ids (OIDs? MIBs?) are consistent across devices of the same model, series, specific to Tripplite, etc.
Specifically, I use this with a 'SMART500RT1u'.


## usage

at a minimum, an SNMP address is needed:

```
SNMP_ADDRESS=172.16.116.98 python3 snmp.py | jq
{
  "ip": "172.16.116.98",
  "load": 138,
  "uptime_days": 26,
  "ac_voltage": 119,
  "battery_temp": 27,
  "mac": "\u0000@",
  "model": "SMART500RT1U"
}
```

the same json can be served on a flask server:

```
SNMP_ADDRESS=10.1.2.3 python3 snmp.py --flask
```

or we can push time-series metrics to InfluxDB:

```
export SNMP_ADDRESS=10.1.2.3
export INFLUX_BUCKET=power
export INFLUX_ORG=defaultorg
export INFLUX_TOKEN=asdfasdf
export INFLUX_URL=http://10.4.5.6:8086
python3 snmp.py --influx
```

though ideally we set-and-forget in kubernetes:
*(terraform manifest shown)*

```
resource "kubernetes_deployment" "ups-metrics" {
  metadata {
    name = "ups-metrics"
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "ups-metrics"
      }
    }
    template {
      metadata {
        labels = {
          app = "ups-metrics"
        }
      }
      spec {
        container {
          image = "images.local:5000/ups-metrics"
          name  = "ups-metrics"
          env {
            name = "SNMP_ADDRESS"
            value = "172.16.116.98"
          }
          env {
            name = "INFLUX_BUCKET"
            value = "power"
          }
          env {
            name = "INFLUX_ORG"
            value = "defaultorg"
          }
          env {
            name = "INFLUX_URL"
            value = "http://influxdb:8086"
          }
          env {
            name = "INFLUX_TOKEN"
            value_from {
              secret_key_ref {
                name = "influx-senders"
                key = "token"
              }
            }
          }
        }
      }
    }
  }
}
```

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

you may have noticed, an old golang version of this is laying around as well.
