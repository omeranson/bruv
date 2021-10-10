FROM python:3.9-slim

WORKDIR /opt/

COPY . .

RUN DEBIAN_FRONTEND=noninteractive apt update && \
	DEBIAN_FRONTEND=noninteractive apt install -y git && \
	DEBIAN_FRONTEND=noninteractive apt clean && \
	pip install "git+https://github.com/ficoos/python-gerrit.git#egg=gerrit" && \ 
	pip install -e .

CMD [ "webruvd" ]

