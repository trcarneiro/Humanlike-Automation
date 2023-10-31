# Use uma imagem base do Ubuntu
FROM ubuntu:latest

# Defina variáveis de ambiente
ENV DISPLAY=:1

# Instale as dependências
RUN apt-get update && \
    apt-get install -y \
    git \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    curl \
    python3-pip \
    python3-selenium \
    python3-venv \
    chromium-chromedriver && \
    curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable pkg-config libcairo2-dev

# Remova qualquer link simbólico ou arquivo existente e crie um novo link simbólico
RUN rm -f /usr/bin/chromedriver && \
    ln -s /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver

# Copie o script para o contêiner
COPY setup.sh /root/setup.sh

# Dê permissão de execução ao script
RUN chmod +x /root/setup.sh

# Execute o script
CMD ["/bin/bash", "/root/setup.sh"]
