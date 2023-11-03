#!/usr/bin/env bash

# Clone o repositório
#git clone https://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@github.com/trcarneiro/WTBOT01.git

# Atualize os pacotes e instale as dependências
#apt-get update
#apt-get install -y unzip xvfb libxi6 libgconf-2-4

# Instale o Google Chrome
#curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
#apt-get update
#apt-get install -y google-chrome-stable

# Instale outras dependências Python
#apt-get install -y python3-pip python3-selenium python3-venv chromium-chromedriver xvfb

# Configurações do Xvfb
#export DISPLAY=:1
#Xvfb $DISPLAY -screen $DISPLAY 1280x1024x16 &

# Instale as dependências do Python
pip install -r requirements.txt
