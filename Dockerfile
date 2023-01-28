from python:3-alpine

copy requirements.txt .

run apk add net-snmp-dev gcc musl-dev &&\
    pip install -r requirements.txt

copy snmp.py .

cmd [ "python3", "snmp.py", "--influx" ]
