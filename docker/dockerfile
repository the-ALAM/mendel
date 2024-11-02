FROM python:3.9

WORKDIR /app

COPY requirements.txt .
COPY .  ./app/

# COPY app/ ./app/app
# COPY sql/ ./app/sql/
# COPY data/ ./app/data/

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client unzip

RUN unzip -o ./app/data/patients_fhir_100.zip -d ./app/data/

EXPOSE 8000

ENV POSTGRES_HOST=db
ENV POSTGRES_PORT=${POSTGRES_PORT}
ENV POSTGRES_DB=${POSTGRES_DB}
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

# CMD ["python", "scheduler.py"]
# CMD ["python", "-m", "app.main", "--interval", "once", "--time", "14:15"]
CMD ["python", "app/main.py", "--interval", "once", "--time", "14:15"]
