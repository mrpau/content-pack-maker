FROM ubuntu:xenial

# install latest python and nodejs
RUN apt-get -y update
RUN apt-get install -y software-properties-common curl
RUN add-apt-repository ppa:voronov84/andreyv
RUN apt-get -y update
RUN apt-get install -y python2.7 python3.5 python-pip git python3-dev

COPY . /ka-lite-content-packs
VOLUME /contentpacks/

RUN pip install virtualenv && virtualenv /contentpackmaker/ --python=python3.5
ENV PATH=/contentpackmaker/bin:$PATH

RUN ls -lh && cd /ka-lite-content-packs && pip install -r requirements_dev.txt
