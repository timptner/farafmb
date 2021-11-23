FROM python:3.9-slim

# Disable buffering
ENV PYTHONUNBUFFERED=1

# Copy project dependencies
COPY requirements.txt /requirements.txt

# Update package manager
RUN python -m pip install --upgrade pip

# Install project dependencies
RUN python -m pip install --no-cache-dir -r /requirements.txt

# Set working directory
RUN mkdir /app/
WORKDIR /app/

# Copy source code into container
COPY . /app/

# Collect static files
RUN DEVELOPMENT_MODE=True python manage.py collectstatic --noinput

# Install python webserver
RUN python -m pip install gunicorn

# Specify public port
EXPOSE 8000

# Start gunicorn webserver as default command
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "farafmb.wsgi:application"]
