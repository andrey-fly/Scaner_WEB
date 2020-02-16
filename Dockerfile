FROM python:3.7

ENV PYTHONUNBUFFERED 1
RUN mkdir /web
WORKDIR /web
COPY requirements.txt /web/
RUN pip3 install -r requirements.txt
COPY . /web/

