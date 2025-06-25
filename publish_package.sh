#!/bin/bash
# publish_package.sh - Script para publicar o pacote humanlike-automation no PyPI

echo "🚀 Publicação do pacote humanlike-automation no PyPI"
echo "=================================================="

# Verificar se estamos no diretório correto
if [ ! -f "setup.py" ]; then
    echo "❌ setup.py não encontrado. Execute no diretório raiz do projeto."
    exit 1
fi

echo "📋 Instalando ferramentas de build..."
python -m pip install --upgrade pip setuptools wheel build twine

echo "🧹 Limpando builds anteriores..."
rm -rf build/ dist/ *.egg-info/

echo "🔍 Validando configuração..."
python setup.py check

echo "🔨 Construindo pacote..."
python -m build

echo "✅ Verificando integridade do pacote..."
python -m twine check dist/*

echo ""
echo "📦 Arquivos gerados:"
ls -la dist/

echo ""
echo "🧪 Para testar primeiro (recomendado):"
echo "   twine upload --repository testpypi dist/*"
echo "   pip install -i https://test.pypi.org/simple/ humanlike-automation"

echo ""
echo "🚀 Para publicar no PyPI principal:"
echo "   twine upload dist/*"

echo ""
echo "✅ Build concluído! Use os comandos acima para publicar."
