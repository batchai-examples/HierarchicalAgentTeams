#!/bin/bash

source .env

export OPENAI_API_KEY
export OPENAI_PROXY_URL
export TAVILY_API_KEY
export HTTPS_PROXY
export HTTP_PROXY

python main.py

