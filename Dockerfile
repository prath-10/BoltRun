FROM python:3.8-alpine

LABEL maintainer="Team Bolt <boltyten@gmail.com>"
LABEL dockerfile-creator="Team Bolt <boltyten@gmail.com>"

RUN addgroup -S raccoon && \
    adduser -S raccoon -G raccoon

RUN apk add --no-cache gcc musl-dev libxml2-dev libxslt-dev nmap nmap-scripts openssl

USER raccoon
WORKDIR /home/raccoon
RUN pip install raccoon-scanner

ENV PATH=/home/raccoon/.local/bin:${PATH}

ENTRYPOINT ["boltrun"]
CMD ["--help"]
