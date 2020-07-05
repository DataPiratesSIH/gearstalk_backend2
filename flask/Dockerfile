FROM python:3.7-slim as base

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r  /app/requirements.txt

ADD . /app
VOLUME /app
# EXPOSE 5000

# CMD ["gunicorn" ,"-w" ,"2" ,"--chdir" ,"/app" ,"app:app", "-b" ,":5000", "--log-level" ,"debug", "--reload"]

# Step 1: Import the Os
# FROM alpine:latest

# Step 2: Install pip and Python Dependencies
# RUN apk add --no-cache python3-dev \
#     && pip3 install --upgrade pip

# # Step 3: Create a Work Directory
# WORKDIR /app

# # Step 4: copy all Project Files
# COPY . /app

# # Step 5: Install all Dependencies for WSGI
# RUN set -e; \
# 	apk add --no-cache --virtual .build-deps \
# 		gcc \
# 		libc-dev \
# 		linux-headers \
# 	; \
# 	pip3 --no-cache-dir install -r requirements.txt; \
# 	apk del .build-deps;

# Step 6:  run the command to start uWSGI
CMD ["gunicorn" , "app.ini"]