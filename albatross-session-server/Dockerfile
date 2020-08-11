FROM python:2.7-alpine as base

RUN apk update
RUN pip install pip --upgrade

FROM base AS build-base

ARG ALBATROSS=albatross-1.42
WORKDIR /build
RUN wget -q http://www.object-craft.com.au/projects/albatross/download/${ALBATROSS}.tar.gz \
	&& pip wheel ${ALBATROSS}.tar.gz

FROM base as final

RUN apk add tzdata
RUN echo "Australia/Melbourne" >/etc/timezone && \
    ln -sf /usr/share/zoneinfo/Australia/Melbourne /etc/localtime

COPY --from=build-base /build/*.whl /tmp/
RUN pip install /tmp/*.whl; rm /tmp/*.whl

CMD /usr/local/bin/albatross session-server --foreground --logfile=/dev/stdout