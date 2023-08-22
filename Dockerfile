FROM python:3.11

WORKDIR /usr/src/app/src

COPY conf/requirements.txt ./conf/requirements.txt
COPY conf/constraints.txt ./conf/constraints.txt

RUN apt-get update \
    && apt-get upgrade -y \
    && pip --no-cache-dir install -r ./conf/requirements.txt -c ./conf/constraints.txt \
    && rm -rf /var/cache/apt

COPY . .

WORKDIR /usr/src/app/src

COPY docker/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
