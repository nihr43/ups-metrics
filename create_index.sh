#!/bin/sh
#
## drops and creates "power" index with mappings.  elasticsearch 6.x

ELASTIC_URL="http://elasticsearch.localnet:9200"

set -e

curl -X DELETE "${ELASTIC_URL}/power?pretty"
curl -X PUT "${ELASTIC_URL}/power?pretty" \
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
    "_doc": {
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
}
'
