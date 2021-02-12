#!/bin/sh

set -x
set -e

if [ ! -d /etc/nginx/ssl ] ; then
  mkdir /etc/nginx/ssl
  ./gen_cert.sh
  mv cert.pem key.pem /etc/nginx/ssl
fi

cp sites-available/* /etc/nginx/sites-available/
cp conf.d/* /etc/nginx/conf.d/
if [ -f /etc/nginx/nginx.conf -a  ! -f /etc/nginx/nginx.conf.back ] ; then
  cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.back
fi
cp nginx.conf /etc/nginx/

rm /etc/nginx/sites-enabled/*
ln -s /etc/nginx/sites-available/victory121-http.conf  /etc/nginx/sites-enabled/victory121-http.conf
ln -s /etc/nginx/sites-available/victory121-https.conf  /etc/nginx/sites-enabled/victory121-https.conf

service nginx reload
