#!/bin/sh

set -x
set -e

if [ -f .inited ] ; then
  exit 0
fi


while ! curl 'localhost:9200' --fail -s  ; do
  echo 'Elasticsearch is not running, sleeping 5s'
  sleep 5
done

curl -XPUT 'localhost:9200/nginx' --data @/nginx_template.json -H'Content-type: application/json'

touch .inited
