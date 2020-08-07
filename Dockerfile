FROM python:2

RUN apt-get update && apt-get install -y libpq5 apache2 postgresql-client python-matplotlib graphviz
RUN pip install pip --upgrade

WORKDIR /build
RUN wget http://www.object-craft.com.au/projects/albatross/download/albatross-1.42.tar.gz
RUN tar xzf albatross-1.42.tar.gz
RUN cd albatross*; python setup.py install

RUN easy_install egenix-mx-base
RUN pip install ocpgdb

WORKDIR /opt/netepi
ADD . .
RUN python install.py appname=collection create_db=false dsn='postgres:example@db::collection:'

EXPOSE 80
CMD apachectl -D FOREGROUND

