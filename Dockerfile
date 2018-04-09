FROM python:alpine3.7
MAINTAINER yatuhashi kei <keyansuiya@gmail.com>

RUN pip install discord
ADD gameplay.py /wolf/gameplay.py
