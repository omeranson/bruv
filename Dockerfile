FROM python:3.9-slim

ARG PROXY_MITM
WORKDIR /opt/

COPY . .

RUN DEBIAN_FRONTEND=noninteractive apt update && \
	DEBIAN_FRONTEND=noninteractive apt install -y git && \
	DEBIAN_FRONTEND=noninteractive apt clean && \
	if [ "$PROXY_MITM" = "true" ]; then \
		git config --global http.sslVerify false; \
                pip install --trusted-host github.com "git+https://github.com/ficoos/python-gerrit.git#egg=gerrit"; \
        else \
		pip install "git+https://github.com/ficoos/python-gerrit.git#egg=gerrit"; \
        fi && \
	pip install -e .

CMD [ "webruvd" ]

