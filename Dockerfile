FROM openjdk:8-alpine

# Install bash
RUN apk add python3

# Copy scripts into place
COPY index /
COPY init /
COPY interact /
COPY search /

# Set working directory
WORKDIR /work