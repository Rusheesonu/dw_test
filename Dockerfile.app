# Dockerfile for Flask app
FROM python:3.9

WORKDIR /app


# Set default environment variables if needed
ENV POSTGRES_DB='dw_test'
ENV POSTGRES_USER='postgres'
ENV POSTGRES_PASSWORD='1234'
ENV POSTGRES_HOST='host.docker.internal' 
ENV POSTGRES_PORT='5432'

# Copy your Flask app code and dependencies
COPY app.py requirements.txt ./

# Create a directory for templates in the image
RUN mkdir -p /app/templates

# Copy the templates directory into the image
COPY templates/ /app/templates/

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "app.py"]
