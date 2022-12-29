
# Base Image
FROM python:3.10.7-slim-bullseye as base

# Python Interpreter Flags
ENV PYTHONUNBUFFERED 1  
ENV PYTHONDONTWRITEBYTECODE 1

# Install os-level dependencies (as root)
RUN apt-get update && apt-get install -y -q --no-install-recommends \
  # dependencies for building Python packages
  build-essential \
  # postgress client (psycopg2) dependencies
  libpq-dev \
  libgdal-dev \
  # mysql client
  default-libmysqlclient-dev \
  # cleaning up unused files to reduce the image size
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# ================================= PRODUCTION =================================
FROM base as production

# Create a directory for the source code and use it as base path
WORKDIR /app

# Create a user to avoid running containers as root in production
RUN useradd -m flask
RUN chown -R flask:flask /app /tmp

# Switch to the non-root user
USER flask
ENV PATH="/home/flask/.local/bin:${PATH}"

COPY requirements requirements
RUN pip install --no-cache --user -r requirements/prod.txt

COPY . .

# ================================= DEVELOPMENT ================================
FROM base as development
WORKDIR /app
COPY requirements requirements
RUN pip install --no-cache -r requirements/dev.txt
COPY . .