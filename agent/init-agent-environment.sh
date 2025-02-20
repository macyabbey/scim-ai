#!/bin/bash

# Install uv on development system
# https://github.com/astral-sh/uv
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
echo 'eval "$(uvx --generate-shell-completion zsh)"' >> ~/.zshrc

# Make sure right version of python install and pinned
uv python install 3.12.8
uv python pin 3.12.8

# Initiatlize the python environment
uv init
# For smolagents
uv add smolagents python-dotenv
# Exporting agent telementry data to pheonix container
uv add opentelemetry-sdk opentelemetry-exporter-otlp openinference-instrumentation-smolagents
# For sql connector agent running on mac os x (note mac on arm is what caused psycopg2-binary instead of psycopg2)
uv add sqlalchemy psycopg2-binary
# For working with "typed" json being returned between tools & agents
uv add pydantic
# For testing
uv add pytest
