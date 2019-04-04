FROM openjdk:8-alpine

# Install bash
RUN apk add python3

# Copy scripts into place
COPY init init
COPY index index
COPY search search

# Set working directory
WORKDIR /work