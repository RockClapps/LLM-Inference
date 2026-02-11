#!/bin/bash

mkdir ollamaBin
cd ollamaBin

rm -r ollama-linux-amd64.tgz bin/ lib/
wget https://github.com/ollama/ollama/releases/download/v0.12.11/ollama-linux-amd64.tgz

tar -xzf ollama-linux-amd64.tgz
