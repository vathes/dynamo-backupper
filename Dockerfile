FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y python3-pip 
RUN apt-get install -y git

RUN pip3 install pandas boto3 google-api-python-client google-auth-httplib2 google-auth-oauthlib

WORKDIR /src