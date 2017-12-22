FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

ADD ./requirements.txt /srv/requirements.txt
RUN pip install -r /srv/requirements.txt

ADD . /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["app.py"]
