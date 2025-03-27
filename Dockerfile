# FROM python:3.12-slim

# WORKDIR /code

# COPY ./requirements.txt /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./app /code/app

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]



FROM public.ecr.aws/amazonlinux/amazonlinux:latest

# Update installed packages
# Install system dependencies
RUN dnf update -y && \
    dnf install -y make && \
    dnf install -y git

# pull official base image
# FROM python:3.12-slim

# Install Python 3.12 (specific version)
RUN dnf install python3.12 -y

# Check the installed Python version
RUN python3.12 --version

# Install Pip3.12
RUN dnf install python3.12-pip -y

# Check the installed Pip version
RUN pip3.12 --version

# Map python and pip commands to installed versions 
RUN ln -s /usr/bin/python3.12 /usr/bin/python & \
    ln -s /usr/bin/pip3.12 /usr/bin/pip

# Map python and pip commands to installed versions 
# RUN echo -e 'alias python="/usr/local/bin/python3.12" \n alias pip="/usr/local/bin/pip3.12"' >> ~/.bashrc

# Apply bashrc edits to current session
# RUN source ~/.bashrc

# Set work directory
WORKDIR /df-data-profile

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Copy certs over
# COPY certs/* /app/

# Create Python Virtual Env
RUN python3.12 -m venv ~/.venv

# Activate Python virt env
RUN source ~/.venv/bin/activate

# Copy code
COPY . /df-data-profile

# install dependencies
RUN make install 

# Show all installed modules
RUN pip3.12 list
RUN pip list

# Expose port for the API
EXPOSE 8080

# run entrypoint sh script or command
ENTRYPOINT ["dp-app-api"]
