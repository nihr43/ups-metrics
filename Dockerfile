FROM alpine:edge

COPY ups-metrics /bin/ups-metrics
RUN chmod +x /bin/ups-metrics
CMD [ "/bin/ups-metrics" ]
