FROM alpine:edge

RUN apk add --no-cache net-snmp-tools coreutils curl
COPY init.sh .
ENTRYPOINT [ "/bin/sh", "init.sh" ]
