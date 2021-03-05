#!/bin/sh

set -x
set -e

if [ -f .inited ] ; then
  exit 0
fi


while ! curl 'localhost:5601/status' --fail -s -o /dev/null  ; do
  echo 'Kibana is not running, sleeping 5s'
  sleep 5
done

curl -s 'localhost:5601/api/saved_objects/_import?overwrite=true'  -H "kbn-xsrf: true" --form file=@/export.ndjson

touch .inited
