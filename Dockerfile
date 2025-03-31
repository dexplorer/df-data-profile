# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.12
# FROM python:${PYTHON_VERSION}-slim AS base

FROM public.ecr.aws/amazonlinux/amazonlinux:latest
ARG PYTHON_VERSION

# Update installed packages and install system dependencies
RUN dnf update -y && \
    dnf install -y make && \
    dnf install -y git && \
    dnf install -y findutils
# findutils is needed for xargs command

# Install python (specific version)
RUN dnf install python${PYTHON_VERSION} -y

# Install pip
RUN dnf install python${PYTHON_VERSION}-pip -y

# Map python and pip commands to installed versions 
RUN ln -s /usr/bin/python${PYTHON_VERSION} /usr/bin/python & \
    ln -s /usr/bin/pip${PYTHON_VERSION} /usr/bin/pip

# Map python and pip commands to installed versions 
# RUN echo -e 'alias python="/usr/local/bin/python3.12" \n alias pip="/usr/local/bin/pip3.12"' >> ~/.bashrc

# Apply bashrc edits to current session
# RUN source ~/.bashrc

# Check the installed python version
RUN python${PYTHON_VERSION} --version

# Check the installed pip version
RUN pip${PYTHON_VERSION} --version

# Set work directory
WORKDIR /df-data-profile

# Set environment variables

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Copy certs over
# COPY certs/* /app/

# Create Python Virtual Env
RUN python${PYTHON_VERSION} -m venv ~/.venv

# Activate Python virt env
RUN source ~/.venv/bin/activate

# Copy the source code into the container.
COPY . /df-data-profile

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
# RUN --mount=type=cache,target=/root/.cache/pip \
#     --mount=type=bind,source=requirements.txt,target=requirements.txt \
#     python -m pip install -r requirements.txt

# ARG CACHEBUST=1
# RUN echo "CACHEBUST"

COPY --from=workspaces utils /packages/utils
COPY --from=workspaces df-metadata /packages/df-metadata
COPY --from=workspaces df-app-calendar /packages/df-app-calendar
COPY --from=workspaces df-config /packages/df-config

# Install app dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    make install 

# Expose the port that the application listens on. 
# This is just for documentation. Port should be exposed when the container is instantiated or via docker publish port.
EXPOSE 80

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/nonexistent" \
#     --shell "/sbin/nologin" \
#     --no-create-home \
#     --uid "${UID}" \
#     appuser

# Add a new user
RUN useradd -m -s /bin/bash app-user

# Set a password (replace with a secure method for production)
# RUN echo "myuser:mypassword" | chpasswd

# Add user to docker group (optional)
# RUN usermod -aG docker app-user

# Switch to the non-privileged user to run the application.
USER app-user

# Run entrypoint sh script or command
ENTRYPOINT ["dp-app-api"]

# Run the application.
# CMD python3 -m uvicorn app:app --host=0.0.0.0 --port=8000



# Reference

# FROM python:3.12-slim

# WORKDIR /code

# COPY ./requirements.txt /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
