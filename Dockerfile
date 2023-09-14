FROM python:3.10-bullseye

WORKDIR /usr/src/app

COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY . .

CMD [ "python", "./src/etherscan.py" ]