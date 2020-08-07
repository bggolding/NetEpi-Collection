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
RUN python install.py appname=collection create_db=false dsn='::collection:'

# this fixes a wacky bug with sysconfig on Debian (https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=783738)
RUN cd /usr/lib/python2.7/; ln -s plat-x86_64-linux-gnu/_sysconfigdata_nd.py .

RUN a2enmod cgi

EXPOSE 80
CMD albatross session-server start && apachectl -D FOREGROUND
