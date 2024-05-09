FROM alpine:3.19  

# Install basic Alpine packages (if needed)
RUN apk add --no-cache --update alpine-base

# Install Python development libraries and upgrade pip
RUN sh -c "apk add python3-dev && pip3 install --upgrade pip"

# Your application code or remaining Dockerfile instructions...
