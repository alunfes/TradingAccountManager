# fastapi/Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /src
VOLUME /src/tmp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--uds", "tmp/uvicorn.sock", "--reload"]

