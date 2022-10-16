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

## usage

`make` knows how to quickly setup the go module, build the project, and run it in docker:

```
$ make
go mod init ups-metrics
go: creating new go.mod: module ups-metrics
go: to add module requirements and sums:
	go mod tidy
go mod tidy
go: finding module for package github.com/gorilla/mux
go: found github.com/gorilla/mux in github.com/gorilla/mux v1.8.0
gofmt main.go | sponge main.go
CGO_ENABLED=0 go build main.go
docker-compose build && docker-compose up
Building ups-metrics
Sending build context to Docker daemon  7.066MB
Step 1/4 : FROM alpine:edge
 ---> 49b6d04814d5
Step 2/4 : COPY main /bin/ups-metrics
 ---> Using cache
 ---> 36f12d294b08
Step 3/4 : RUN chmod +x /bin/ups-metrics
 ---> Using cache
 ---> 008eb8db5abd
Step 4/4 : CMD [ "/bin/ups-metrics" ]
 ---> Using cache
 ---> 78cfd77c81e6
Successfully built 78cfd77c81e6
Successfully tagged images.local:5000/ups-metrics:latest
Starting ups-metrics_ups-metrics_1 ... done
Attaching to ups-metrics_ups-metrics_1
```
