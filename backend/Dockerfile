FROM python:3.6
MAINTAINER dilipjoshis98@gmail.com
ENV PYTHONUNBUFFERED 1
RUN mkdir /backend
WORKDIR /backend
ADD Himalaya/requirements.txt /backend
RUN pip3 install -r requirements.txt
ADD . /backend/