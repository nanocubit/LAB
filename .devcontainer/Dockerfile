FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends curl jq git-lfs && rm -rf /var/lib/apt/lists/*
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y --profile minimal
ENV PATH="/home/vscode/.local/bin:/home/vscode/.cargo/bin:${PATH}"
