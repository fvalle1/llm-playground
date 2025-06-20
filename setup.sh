#!/bin/bash

mkdir -p data
mkdir -p snapshots
python3 -c "import nltk; nltk.download('gutenberg', download_dir='$PWD')"

ollama serve & > 2>&1

docker compose up
