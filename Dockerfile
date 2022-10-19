FROM alpine:edge

COPY main /bin/ups-metrics
RUN chmod +x /bin/ups-metrics
CMD [ "/bin/ups-metrics" ]
