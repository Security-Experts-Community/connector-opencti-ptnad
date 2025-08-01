FROM python:3.11-alpine
ENV CONNECTOR_TYPE=STREAM

# Copy the worker
COPY src /opt/opencti-connector-ptnad

# Install Python modules
RUN apk --no-cache add git build-base libmagic libffi-dev libxml2-dev libxslt-dev
RUN cd /opt/opencti-connector-ptnad && \
    pip3 install --no-cache-dir -r requirements.txt && \
    apk del git build-base

# Expose and entrypoint
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]