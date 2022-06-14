FROM alpine:edge

RUN apk add --no-cache py3-pip python3-dev gcc musl-dev net-snmp-dev
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY snmp.py .
ENTRYPOINT [ "/usr/bin/python3", "snmp.py" ]
