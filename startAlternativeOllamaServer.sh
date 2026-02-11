#!/bin/bash


OLLAMA_HOST="127.0.0.1:11435" \
  OLLAMA_MODELS="models" \
  ollama serve &>/dev/null &
