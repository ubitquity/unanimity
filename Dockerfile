FROM ubuntu:18.04
ENV PYTHONUNBUFFERED 1
RUN set -e;


RUN apt-get update
RUN apt-get install -y python3-pip \
        build-essential \
        libssl-dev \
        autoconf \
        libtool \
        libffi-dev \
        libgmp-dev \
        libsecp256k1-dev \
        pkg-config \
        software-properties-common

ADD . /app/
WORKDIR /app/

RUN pip3 install -r requirements.txt

RUN add-apt-repository -y ppa:ethereum/ethereum
RUN apt-get install -y ethereum solc
RUN pip3 install bitcoin==1.1.42
EXPOSE 8080


CMD ["python3", "manage.py", "runserver", "0:8080"]