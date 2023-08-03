FROM python:3.11

COPY conf/requirements.txt ./conf/requirements.txt
COPY conf/constraints.txt ./conf/constraints.txt

RUN apt-get update \
    && apt-get upgrade -y \
    && pip --no-cache-dir install -r ./conf/requirements.txt -c ./conf/constraints.txt \
    && rm -rf /var/cache/apt

COPY . .

CMD [ "python", "./main.py" ]
