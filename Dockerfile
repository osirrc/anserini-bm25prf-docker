FROM maven:3.6.1-jdk-8-alpine AS builder

WORKDIR /Anserini/
COPY Anserini .
RUN  mvn clean package appassembler:assemble 


FROM openjdk:8-alpine

# Install bash

RUN apk --no-cache add python3

# Set working directory
WORKDIR /work

COPY --from=builder /Anserini .

RUN pip3 install -r requirements.txt

# Copy scripts into place
COPY index /
COPY init /
COPY interact /
COPY search /
COPY *.py /
COPY data /

