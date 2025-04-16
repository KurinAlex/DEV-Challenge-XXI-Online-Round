FROM python

# set directory to install vosk model
WORKDIR /usr/share/vosk

# install vosk speech recognition model
RUN curl -L -o vosk-model.zip https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip && \
    unzip vosk-model.zip && \
    rm vosk-model.zip

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# install ffmpeg
RUN apt-get update && apt-get -y install ffmpeg libavcodec-extra

# copy project
COPY ./apiproject .

# load hugging face transformer models
RUN python apiapp/pipelines.py