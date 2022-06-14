#!/bin/sh
#
## drops and creates "power" index with mappings.  elasticsearch 6.x

ELASTIC_URL="https://elasticsearch.local:9200"

set -e

curl -k -u elastic -X DELETE "${ELASTIC_URL}/power?pretty"
curl -k -u elastic -X PUT "${ELASTIC_URL}/power?pretty" \
     -H 'Content-Type: application/json' \
     -d '
{
  "settings": {
    "index": {
      "number_of_shards": 2,
      "number_of_replicas": 1
    }
  },
  "mappings": {
    "properties": {
      "@timestamp": {
        "type": "date"
      },
      "temp": {
        "type": "integer"
      },
      "watts": {
        "type": "integer"
      }
    }
  }
}
'
