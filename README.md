# DEV-Challenge-XXI-Online-Round

This solution is written on [Python](https://www.python.org/) with use of [Django](https://www.djangoproject.com/), [Django REST framework](https://www.django-rest-framework.org/), [PostgreSQL](https://www.postgresql.org/) database and [Celery](https://docs.celeryq.dev/) task queue with [RabbitMQ](https://www.rabbitmq.com/) message brocker. Also, it utilizes [Vosk](https://alphacephei.com/vosk/) for voice-to-text translation and various [Hugging Face transformer](https://huggingface.co/docs/transformers/index) models for natural language processing.

## Getting started

It is much easier to run application using Docker, since everything is already configured and needs just Docker to be installed.

**Important:** Please consider .env file, which contains environment variables configured for running from Docker. If you want to start application natively, some variables needs to be changed, which is covered in [Run natively](#run-natively) section.

### Run with Docker

1. Intall Docker from <https://www.docker.com/get-started/>.

2. To build and start Docker dontainer:

    ``` bash
    docker compose -f "docker-compose.yml" up
    ```

    **Note:** It may take some time (around 5-10 minutes on average setup and Internet connection) for compose operation to finish because of pre-loading all machine learning models and libraries (such as PyTorch).

3. Wait for message from container output, which states your server is now running on <http://localhost:8080/>.

4. To stop container:

    ``` bash
    docker compose -f "docker-compose.yml" stop
    ```

    or to stop and remove all images, volumes etc.:

    ``` bash
    docker compose -f "docker-compose.yml" down
    ```

### Run natively

1. Install Python with pip from <https://www.python.org/downloads/>.

2. Install all neccessary packages (ensure you are in application folder):

    ``` bash
    pip install -r requirements.txt
    ```

3. Install PostgreSQL from <https://www.postgresql.org/download/>.

4. Create 'devchallenge' database using psql terminal:

    ``` sql
    CREATE DATABASE devchallenge
    ```

5. Install RabbitMQ from <https://www.rabbitmq.com/docs/download>.

6. Ensure .env file have relevant information about PostgreSQL and RabbitMQ ports/logins/passwords. Ensure they have 'localhost' host.

7. Install ffmpeg from <https://www.ffmpeg.org/download.html>. For installing on Windows please follow [this](https://phoenixnap.com/kb/ffmpeg-windows) guide.

8. (Optional) It is recommended to pre-load machine learning models (so they won't take time to install on first api calls):
    - Install and unzip preferred vosk model from <https://alphacephei.com/vosk/models> (vosk-model-small-en-us-0.15 is a recommended one). Specify its' location using VOSK_MODEL_PATH environment variable in .env file.
    - Load Hugging Face transformer models:

        ``` bash
        python apiproject/apiapp/pipelines.py
        ```

9. Move to apiproject directory:

    ``` bash
    cd apiproject
    ```

10. Run database migrations:

    ``` bash
    python manage.py migrate
    ```

11. (Optional) Seed database with initial data:

    ```bash
    python manage.py loaddata seed-data.json
    ```

12. In 'apiproject' directory start two terminals.

13. In first terminal start celery worker:

    ``` bash
    celery -A apiproject worker -l INFO
    ```

14. In second terminal start server:

    ``` bash
    python manage.py runserver $DJANGO_PORT
    ```

## Tests

Tests are running from Docker to avoid comples setup.

1. Intall Docker from <https://www.docker.com/get-started/>.

2. To build and start Docker dontainer:

    ``` bash
    docker compose -f "docker-compose.test.yml" up
    ```

    **Note:** It may take some time (around 5-10 minutes on average setup and Internet connection) for compose operation to finish because of pre-loading all machine learning models and libraries (such as PyTorch).

3. Check output from created container to see testing results.

4. To stop container:

    ``` bash
    docker compose -f "docker-compose.test.yml" stop
    ```

    or to stop and remove all images, volumes etc.:

    ``` bash
    docker compose -f "docker-compose.test.yml" down
    ```

## Covered edge cases

- Using streaming for loading files, which helps to save memory for large files.

- All text-processing tasks run in the background to avoid blocking main thread.

- Waiting for initial call processing to finish before applying any recategorizing. Fow example, if new category was added while call audio was still processed, categories will be updated only after text analysis finish.

## Next steps

There are some drawbacks of system current version, such as:

- If several category-updating operations were run at once, then it will create same amount of recategorizing tasks for every call instance without guarantee to finish in needed order.

- Relatively long Docker build (as mentioned in [Run with Docker](#run-with-docker) section).

Fixing these problems will enhance system to work correctly and faster.
