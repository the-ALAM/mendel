FROM python:3.9

WORKDIR /app

COPY requirements.txt .
COPY src/ .
COPY sql/ ./sql/
COPY data/ ./data/

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client

EXPOSE 8000

ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=mendel
ENV POSTGRES_USER=mendel
ENV POSTGRES_PASSWORD=zPO5uhF4VDjm

# CMD ["python", "scheduler.py"]
CMD ["python", "main.py", "--interval", "once", "--time", "14:15"]
