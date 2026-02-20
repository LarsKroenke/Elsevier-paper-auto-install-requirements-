#!/usr/bin/env bash
set -euo pipefail

sudo apt-get install -y \
  build-essential \
  procps \
  curl \
  file \
  git

NONINTERACTIVE=1 CI=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv bash)"' >> /home/codespace/.bashrc
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv bash)"

brew install --cask font-maple-mono

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip ipykernel

.venv/bin/python -m pip install \
  pandas \
  numpy \
  matplotlib \
  pubchempy \
  pint \
  pint-pandas \
  latexify-py \
  scienceplots \
  mol2chemfigPy3

