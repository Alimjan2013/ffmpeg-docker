# Dockerfile

FROM gcr.io/buildpacks/google-24/run

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    MY_VARIABLE="This is a default value"

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3.12 \
        python3.12-venv \
        python3.12-pip \
        ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Create virtual environment and install Python dependencies
RUN python3.12 -m venv $VIRTUAL_ENV

# If you have a requirements.txt, use this:
# COPY requirements.txt /app/
# RUN . $VIRTUAL_ENV/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Otherwise, install directly:
RUN . $VIRTUAL_ENV/bin/activate && \
    pip install --upgrade pip && \
    pip install flask requests boto3 ffmpeg-python==0.2.0

# Copy your application code
COPY server.py /app/server.py

EXPOSE 5000

# Optionally switch to a non-root user for security
# RUN useradd --create-home appuser
# USER appuser

ENTRYPOINT ["python3.12", "server.py"]
