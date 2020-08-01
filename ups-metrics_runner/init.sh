#!/bin/sh

set -e

query_snmp() {
  local _ip="$1"
  local _mib="$2"
  local _res=""

  _res=$(snmpwalk -v2c \
                  -c tripplite \
                  "$_ip" \
                  "$_mib" \
           | awk '{print $NF}')

  echo "$_res"
}

post_doc() {
  local _ip="$1"
  local _index="$2"
  local _timestamp="$3"
  local _field="$4"
  local _val="$5"

  curl -H "Content-Type: application/json" \
       -X POST "${_ip}/${_index}/_doc" \
       -d "{ \"@timestamp\" : \"${_timestamp}\", \"${_field}\" : ${_val}}"
}

power_raw=$(query_snmp $SNMP_ADDRESS iso.3.6.1.2.1.33.1.4.4.1.5.1)
percent=$(awk -v p="$power_raw" 'BEGIN {print p/1000}')
watts=$(awk -v p="$percent" 'BEGIN {print 300*p}')

input_voltage=$(query_snmp $SNMP_ADDRESS iso.3.6.1.2.1.33.1.3.3.1.3.1)
temp=$(query_snmp $SNMP_ADDRESS iso.3.6.1.2.1.33.1.2.7.0)

timestamp="$(date --iso-8601='minutes')"

post_doc "$ELASTIC_URL" "$ELASTIC_INDEX" "$timestamp" "temp" "$temp"
post_doc "$ELASTIC_URL" "$ELASTIC_INDEX" "$timestamp" "watts" "$watts"
