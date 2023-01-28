from python:3-slim

copy snmp.py .
copy requirements.txt .

run apt update &&\
    apt install -y libsnmp-dev gcc &&\
    pip install -r requirements.txt

cmd [ "python3", "snmp.py", "--influx" ]
