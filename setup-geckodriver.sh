#!/bin/bash

# Download the geckodriver tar
wget https://github.com/mozilla/geckodriver/releases/download/v0.20.1/geckodriver-v0.20.1-linux64.tar.gz

# Unzip the binary
tar -xzvf geckodriver-v0.20.1-linux64.tar.gz

# Set geckodriver binary in your path
sudo mv geckodriver /usr/local/bin
