# use base python image with python 3.5
FROM python:3.10

# add requirements.txt to the image
ADD requirements.txt /app/requirements.txt

# set working directory to /app/
WORKDIR /app/

# install python dependencies
RUN pip install -U -r requirements.txt

# create unprivileged user
RUN adduser --disabled-password --gecos '' myuser
