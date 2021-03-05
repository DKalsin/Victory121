FROM nginx:1.19.6-alpine

COPY ./gen_cert.sh ./gen_cert.sh
RUN rm /etc/nginx/conf.d/* \
  && apk add openssl \
  && ./gen_cert.sh \
  && ln -sf /dev/stdout /var/log/nginx/access.log \
  && ln -sf /dev/stderr /var/log/nginx/error.log

COPY ./sites-available/victory* /etc/nginx/sites-enabled/
COPY ./conf.d/ /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/
