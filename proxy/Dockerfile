FROM paulczar/omgwtfssl as certificate-generator

ENV SSL_SUBJECT=netepi.object-craft.com.au
WORKDIR /tmp/certs
RUN /usr/local/bin/generate-certs


FROM nginx:alpine

RUN apk add tzdata
RUN cp /usr/share/zoneinfo/Australia/Melbourne /etc/localtime
RUN echo "Australia/Melbourne" >/etc/timezone

RUN rm /etc/nginx/conf.d/*
COPY --from=certificate-generator /tmp/certs/cert.pem /tmp/certs/key.pem /etc/nginx/conf.d/netepi/

COPY index.html /etc/nginx/html/index.html

COPY netepi-proxy.conf /etc/nginx/conf.d
RUN mkdir -p /tmp/nginx/cache && chown nginx.nginx /tmp/nginx/cache