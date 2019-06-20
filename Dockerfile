FROM maven:3.6.1-jdk-8-alpine AS builder

WORKDIR /Anserini/
COPY Anserini .
RUN  mvn clean package appassembler:assemble 

FROM openjdk:8-alpine

RUN apk add --no-cache musl-dev linux-headers g++ 

RUN apk --no-cache add python3 python3-dev make cmake

COPY requirements.txt /
RUN pip3 install --no-cache-dir -r  requirements.txt

COPY --from=builder /Anserini /Anserini
RUN cd Anserini/eval && tar xzf trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make

RUN mkdir /trained

# Copy scripts into place
COPY index /
COPY init /
COPY interact /
COPY search /
COPY train / 
COPY *.py /

