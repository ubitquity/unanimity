FROM ubuntu:18.04
ENV PYTHONUNBUFFERED 1
RUN set -e;

RUN apt-get update && apt-get install -y python3-pip \
        build-essential \
        libssl-dev \
        autoconf \
        libtool \
        libffi-dev \
        libgmp-dev \
        libsecp256k1-dev \
        pkg-config \
        software-properties-common \
        libz3-dev

ADD requirements.txt /app/requirements.txt
WORKDIR /app/

RUN pip3 install -r requirements.txt

ADD . /app/

RUN apt-get update && apt-get -y install wget unzip
RUN wget --output-document=/tmp/solc.zip https://github.com/ethereum/solidity/releases/download/v0.4.24/solidity-ubuntu-trusty.zip
RUN unzip /tmp/solc.zip -d /tmp/
RUN cp /tmp/solc /usr/bin/solc
RUN cp /tmp/lllc /usr/bin/lllc
RUN chmod +x /usr/bin/solc
RUN chmod +X /usr/bin/lllc
RUN pip3 install bitcoin==1.1.42
EXPOSE 8080


CMD "/app/run.sh"
