FROM python:3.14 AS base


WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app


FROM base AS prod
CMD ["fastapi", "run", "app/main.py", "--port", "80"]

FROM base AS dev
CMD ["fastapi", "dev", "app/main.py", "--port", "80", "--host", "0.0.0.0"]

EXPOSE 80

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]