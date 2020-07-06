FROM python:3.7-slim

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r  /app/requirements.txt

ADD . /app
VOLUME /app
# EXPOSE 5000

# CMD ["gunicorn" ,"-w" ,"2" ,"--chdir" ,"/app" ,"app:app", "-b" ,":8080", "--log-level" ,"debug", "--reload"]
#CMD ["gunicorn" , "app.ini"]