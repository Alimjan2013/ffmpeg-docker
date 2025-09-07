FROM jrottenberg/ffmpeg:8-alpine

# The image already contains ffmpeg/ffprobe; no need to install ffmpeg again.
# Install Python runtime and pip.
USER root
RUN apt-get update \
 && apt-get install -y ca-certificates python3 python3-pip \
 && rm -rf /var/lib/apt/lists/*

# Optional: make "python" available
RUN ln -sf /usr/bin/python3 /usr/bin/python || true

# Python libs
RUN pip3 install flask requests boto3 ffmpeg-python==0.2.0

# App
WORKDIR /app
COPY server.py /app/server.py

EXPOSE 5000
ENV MY_VARIABLE="This is a default value"
CMD ["python3", "server.py"]