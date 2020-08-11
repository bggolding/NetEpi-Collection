#------------------------------------------------------------------------------
# Build the base image (minimal distro packages needed to run)
FROM python:2.7-slim AS base

# DO NOT apt-get any packages that depend on python when using the python
# base images - these images do not have a debian python package installed,
# and installing a package that depends on python will install the debian
# python, breaking the image python.

RUN apt-get update && apt-get install -y libpq5 apache2 libapache2-mod-fcgid wget less
RUN pip install pip --upgrade

#------------------------------------------------------------------------------
# Create a transient layer with dev tools to build binary python packages
FROM base AS build-base
ARG ALBATROSS=albatross-1.42

RUN apt-get install -y gcc python-dev libpq-dev

WORKDIR /build
RUN pip wheel ocpgdb
RUN wget -q http://www.object-craft.com.au/projects/albatross/download/${ALBATROSS}.tar.gz \
	&& pip wheel ${ALBATROSS}.tar.gz
RUN pip wheel matplotlib graphviz

#------------------------------------------------------------------------------
# Revert to building from the smaller base image for the rest of the process
FROM base AS final

COPY --from=build-base /build/*.whl /tmp/
RUN pip install /tmp/*.whl; rm /tmp/*.whl

RUN easy_install egenix-mx-base
#RUN apt-get install -y libapache2-mod-python

WORKDIR /src
ADD . .
RUN python install.py \
	appname=collection \
	create_db=false dsn='::collection:' \
	html_target=/var/www/html/collection

WORKDIR /usr/lib/cgi-bin/collection

RUN a2enmod cgi

COPY deploy/apache.conf /etc/apache2/sites-enabled/netepi-collection.conf

EXPOSE 80
CMD albatross session-server start \
    && chown www-data:www-data /usr/lib/cgi-bin/collection/db \
    && chmod ug+w /usr/lib/cgi-bin/collection/db \
	&& (sleep 5; yes 00NetEpi | python /src/tools/compile_db.py '::collection:' /usr/lib/cgi-bin/collection) \
	&& apachectl -D FOREGROUND
