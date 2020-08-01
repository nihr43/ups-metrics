FROM alpine:edge

RUN apk add --no-cache py3-pip python3-dev gcc musl-dev net-snmp-dev
RUN pip3 install easysnmp
COPY snmp.py .
ENTRYPOINT [ "/usr/bin/python3", "snmp.py" ]
