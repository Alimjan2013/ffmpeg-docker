FROM jrottenberg/ffmpeg:8.0-nvidia

# The image already contains ffmpeg/ffprobe; no need to install ffmpeg again.
# Install Python runtime and pip.
USER root
RUN apt-get update \
 && apt-get install -y ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Optional: make "python" available
RUN ln -sf /usr/bin/python3 /usr/bin/python || true


# Python libs: use a virtual environment to avoid system pip restrictions
RUN pip install flask requests boto3 ffmpeg-python==0.2.0

# App
WORKDIR /app
COPY server.py /app/server.py

EXPOSE 5000
ENV MY_VARIABLE="This is a default value"
CMD ["python", "server.py"]