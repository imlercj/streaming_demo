# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# No system dependencies needed when using psycopg2-binary

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN \
 apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

# Copy the Python script into the container
COPY . .

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Ensure the script waits for PostgreSQL to be ready before running
#CMD ["sh", "-c", "sleep 5 && python -u airquality_ingest.py"]
CMD ["sh", "-c", "sleep 5 && python -u wind_data_ingest.py"]
