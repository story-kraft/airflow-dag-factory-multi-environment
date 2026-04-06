FROM apache/airflow:2.10.3-python3.11

USER root

# Install system dependencies (only if really needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy requirements first (better layer caching)
COPY requirements.txt /

# Install Python dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Copy DAGs and configs
COPY dags/ /opt/airflow/dags/
COPY config/ /opt/airflow/config/

# Environment variables
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV ENV=dev

# Optional: set PYTHONPATH
ENV PYTHONPATH="/opt/airflow"

# Healthcheck (scheduler check)
HEALTHCHECK CMD airflow jobs check --job-type SchedulerJob --hostname "$HOSTNAME"