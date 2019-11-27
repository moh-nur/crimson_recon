FROM alpine:3.10

# Setup OWASP amass

# installing OWASP amass
ENV amass_ver v3.3.1
ENV amass ${amass_ver}/amass_${amass_ver}_linux_amd64.zip

RUN apk update && apk add \
    curl \
    git \
    whois \
    python3 \
    vim && \
    mkdir ~/tools && \
	wget -O ~/tools/amass.zip -P ~/tools/ https://github.com/OWASP/Amass/releases/download/${amass} && \
	unzip ~/tools/amass.zip -d ~/tools && \
	mv ~/tools/amass_${amass_ver}_linux_amd64 ~/tools/amass && \
	rm ~/tools/amass.zip

# installing python dependencies
RUN pip3 install beautifulsoup4 py-altdns

# installing go ...
RUN apk add --no-cache --virtual .build-deps bash gcc musl-dev openssl go

# Install gobuster
RUN go get github.com/OJ/gobuster && \
	export GOPATH=$HOME/go && \
	export PATH=$PATH:$GOROOT/bin:$GOPATH/bin && \
	mkdir ~/wordlists && \
	wget https://github.com/danielmiessler/SecLists/raw/master/Discovery/DNS/subdomains-top1million-5000.txt

ENTRYPOINT ["~/tools"]