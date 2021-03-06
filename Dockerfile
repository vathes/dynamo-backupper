FROM python:slim-buster

RUN pip3 install pandas boto3 google-api-python-client google-auth-httplib2

COPY ./ /src
RUN pip3 install /src

WORKDIR /src