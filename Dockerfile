# syntax=docker/dockerfile:1

# ARG PYTHON_VERSION=3.12
# FROM python:${PYTHON_VERSION}-slim AS base

FROM public.ecr.aws/amazonlinux/amazonlinux:latest
ARG PYTHON_VERSION
ARG CONTAINER_PORT

# Update installed packages and install system dependencies
RUN dnf update -y && \
    dnf install -y make && \
    dnf install -y git && \
    dnf install -y findutils && \
    dnf install -y tree
# findutils is needed for xargs command
# shadow-utils is needed for useradd command
# && \ dnf install -y shadow-utils

# Install python
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

# Copy the application dependencies
COPY ./pyproject.toml /df-data-profile
COPY ./Makefile /df-data-profile

# Copy the app dependency source code into the container.
COPY --from=workspaces utils /packages/utils
COPY --from=workspaces df-metadata /packages/df-metadata
COPY --from=workspaces df-app-calendar /packages/df-app-calendar
COPY --from=workspaces df-config /packages/df-config

# Install app dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    make install 

# Copy the app source code into the container.
COPY . /df-data-profile

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
# RUN --mount=type=cache,target=/root/.cache/pip \
#     --mount=type=bind,source=requirements.txt,target=requirements.txt \
#     python -m pip install -r requirements.txt

# Install app 
RUN --mount=type=cache,target=/root/.cache/pip \
    make install 

# Expose the port that the application listens on. i.e. container port
# This is just for documentation. Port should be exposed when the container is instantiated or via docker publish port.
EXPOSE ${CONTAINER_PORT}

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
RUN useradd -m -s /bin/bash app-user
# RUN /usr/sbin/useradd -m -s /bin/bash app-user

# Switch to the non-privileged user to run the application.
USER app-user

# Run the application. 
# ENTRYPOINT ["dp-app-api"]

# Run the application.
CMD ["dp-app-api"]
# CMD ["dp-app-api", "--debug"]
# CMD ["dp-app-api", "--debug", "y"]
