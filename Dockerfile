FROM ubuntu:latest
MAINTAINER Коцеруба Вячеслав
RUN apt-get update -y
RUN apt-get update && apt-get -y install python3.8 python3.8-dev
RUN apt-get -y install python3-pip
COPY . /app
WORKDIR /app
RUN pip3 install pandas datetime flask
ENTRYPOINT ["python3"]
CMD ["main.py" ,"--host=0.0.0.0"]