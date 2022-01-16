# Use ubuntu instead of python for faster compilation
FROM ubuntu:20.04 AS builder

# Disable user input
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    python3.9 python3.9-dev python3.9-venv python3-pip python3-wheel build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
# (using final folder name to avoid path conflicts with packages)
RUN python3.9 -m venv /home/farafmb/venv
ENV PATH="/home/farafmb/venv/bin:$PATH"

# Install requirements (seperate from source code to benefit from docker caching)
COPY ./requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip wheel setuptools
RUN python -m pip install --no-cache-dir -r requirements.txt

# Use seperate stages to only copy compiled packages
FROM ubuntu:20.04 AS runner
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    python3.9 python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up dedicated user
RUN useradd --create-home farafmb
COPY --from=builder /home/farafmb/venv /home/farafmb/venv
USER farafmb

# Set up application directory
RUN mkdir /home/farafmb/code
WORKDIR /home/farafmb/code

# Copy source code into container
# (Make sure to exclude all unnecessary code within .dockerignore)
COPY . .

EXPOSE 5000

# Configure python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Activate virtual environment
ENV VIRTUAL_ENV=/home/farafmb/venv
ENV PATH="/home/farafmb/venv/bin:$PATH"

# /dev/shm is mapped to shared memory and should be used for gunicorn heartbeat
# this will improve performance and avoid random freezes
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "-k", "gevent", "--worker-tmp-dir", "/dev/shm", "farafmb.wsgi"]
