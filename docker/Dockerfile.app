FROM python

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.app.txt .
RUN pip install -r requirements.app.txt

# copy project
COPY ./apiproject .