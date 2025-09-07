# ffmpeg - http://ffmpeg.org/download.html
#
# From https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu
#
# https://hub.docker.com/r/jrottenberg/ffmpeg/
#
#
# Stage 1: Build
# FROM       ubuntu:24.04 AS builder

# WORKDIR     /tmp/workdir

# COPY generate-source-of-truth-ffmpeg-versions.py /tmp/workdir
FROM gcr.io/buildpacks/google-24/run
USER root
RUN apt-get -y update
RUN apt-get install -y python3-12 python3-12-pip
RUN pip3-12 install flask requests boto3 ffmpeg-python==0.2.0

COPY server.py /app/server.py
WORKDIR /app
EXPOSE 5000
# Set an environment variable
ENV MY_VARIABLE="This is a default value"
CMD ["python3-12", "server.py"]

