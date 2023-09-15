FROM python:3.10-bullseye

WORKDIR /usr/src/app

COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY . .
ARG DOCKER=1
CMD [ "python", "./src/trueblocks.py" ]