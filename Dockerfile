FROM ubuntu:16.04
MAINTAINER ash.d.wilson@gmail.com

RUN apt-get update && apt-get upgrade -y && apt-get install -y\
    python \
    python-pip

RUN pip install requests
RUN pip install boto3

COPY sitch/ /app/sitch

WORKDIR /app/sitch
CMD ["/usr/bin/python", "/app/sitch/runner.py"]
