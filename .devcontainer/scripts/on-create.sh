#!/usr/bin/env bash
set -euo pipefail

sudo apt-get update
sudo apt-get install -y \
  texlive \
  texlive-science \
  texlive-latex-extra \
  texlive-bibtex-extra \
  biber \
  latexmk \
  texlive-lang-german \
  texlive-latex-base texlive-latex-recommended texlive-fonts-recommended \
  dvipng cm-super texlive-pictures \
  texlive-latex-extra texlive-fonts-extra dvisvgm ghostscript 
