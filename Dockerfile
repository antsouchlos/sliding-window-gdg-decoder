FROM ubuntu:24.04

# Set up environment

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    UV_CACHE_DIR="/tmp/uv-cache"

# Install basic dependencies

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-venv \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    python3.12-dev

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set up python environment

WORKDIR /tmp/sw-gdg

RUN uv venv /opt/venv --python 3.12
ENV VIRTUAL_ENV=/opt/venv

COPY . /tmp/sw-gdg
RUN uv pip install .
RUN uv pip install matplotlib ldpc jupyter

WORKDIR /root

RUN chmod -R 755 /opt/venv
RUN mkdir -p /tmp/uv-cache && chmod -R 777 /tmp/uv-cache
