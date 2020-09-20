FROM python:slim-buster

RUN pip3 install pandas boto3 google-api-python-client google-auth-httplib2 pytest --no-cache-dir

COPY ./dynamo_backupper /src/dynamo_backupper
COPY ./setup.py /src
RUN pip3 install /src

WORKDIR /src

ENTRYPOINT ["python3", "./scripts/main.py"]