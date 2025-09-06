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
FROM gcr.io/buildpacks/builder
USER root
RUN apt-get -y update
RUN apt-get install -y ffmpeg python3 python3-pip
RUN pip3 install flask requests ffmpeg-python==0.2.0
COPY server.py /app/server.py
WORKDIR /app
EXPOSE 5000
CMD ["python3", "server.py"]

