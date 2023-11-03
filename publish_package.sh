#!/bin/bash

# Parar o script se algum comando falhar
set -e

# Obter a versão atual do pacote a partir do setup.py
VERSION=$(python3 -c "import re; \
                     setup_file='setup.py'; \
                     version_line = [line for line in open(setup_file) if 'version=' in line][0]; \
                     print(re.search(r\"(?<=version=\')\d+\.\d+\.\d+.*(?=\')\", version_line).group(0))")

echo "Versão atual: $VERSION"

# Atualizar o histórico de mudanças
echo "Atualize o arquivo CHANGELOG.md ou HISTORY.txt agora e pressione enter quando estiver pronto."
read

# Geração de distribuição
echo "Gerando distribuição..."
python3 setup.py sdist bdist_wheel

# Publicação no PyPI
echo "Publicando no PyPI..."
pip install twine
#twine upload dist/*

# Tag no Git
echo "Criando tag no Git..."
git tag -a "v$VERSION" -m "Versão $VERSION"
git push origin "v$VERSION"

# Commit e push das mudanças
echo "Fazendo push das alterações para o repositório..."
git add .
git commit -m "Prepare release $VERSION"
git push origin main

echo "Publicação concluída com sucesso."
