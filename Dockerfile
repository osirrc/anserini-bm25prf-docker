FROM openjdk:8-alpine

# Copy scripts into place
COPY init init
COPY index index
COPY train train
COPY search search

# Set working directory
WORKDIR /work
