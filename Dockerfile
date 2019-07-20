FROM alpine:3.10

# Setup OWASP amass

ENV amass_ver 3.0.18
ENV amass ${amass_ver}/amass_${amass_ver}_linux_amd64.zip

RUN apk update && apk add \
    curl \
    git \
    vim && \
    mkdir ~/tools && \
	wget -O ~/tools/amass.zip -P ~/tools/ https://github.com/OWASP/Amass/releases/download/${amass} && \
	unzip ~/tools/amass.zip -d ~/tools && \
	mv ~/tools/amass_${amass_ver}_linux_amd64 ~/tools/amass && \
	rm ~/tools/amass.zip