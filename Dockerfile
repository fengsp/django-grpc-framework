FROM python:3.8

WORKDIR /opt/code

RUN pip install poetry

# RUN poetry init