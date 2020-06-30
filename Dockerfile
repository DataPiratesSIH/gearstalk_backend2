FROM python:3.7-slim as base

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r  /app/requirements.txt

ADD . /app
VOLUME /app
EXPOSE 5000

CMD ["gunicorn" ,"-w" ,"2" ,"--chdir" ,"/app" ,"app:app", "-b" ,":5000", "--log-level" ,"debug", "--reload"]
