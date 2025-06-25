@echo off
REM publish_package.bat - Script para publicar o pacote humanlike-automation no PyPI (Windows)

echo 🚀 Publicação do pacote humanlike-automation no PyPI
echo ==================================================

REM Verificar se estamos no diretório correto
if not exist "setup.py" (
    echo ❌ setup.py não encontrado. Execute no diretório raiz do projeto.
    pause
    exit /b 1
)

echo 📋 Instalando ferramentas de build...
python -m pip install --upgrade pip setuptools wheel build twine

echo 🧹 Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"

echo 🔍 Validando configuração...
python setup.py check
if errorlevel 1 (
    echo ❌ Erro na validação do setup.py
    pause
    exit /b 1
)

echo 🔨 Construindo pacote...
python -m build
if errorlevel 1 (
    echo ❌ Erro durante o build do pacote
    pause
    exit /b 1
)

echo ✅ Verificando integridade do pacote...
python -m twine check dist/*
if errorlevel 1 (
    echo ❌ Pacote falhou na verificação
    pause
    exit /b 1
)

echo.
echo 📦 Arquivos gerados:
dir dist

echo.
echo 🧪 Para testar primeiro (recomendado):
echo    twine upload --repository testpypi dist/*
echo    pip install -i https://test.pypi.org/simple/ humanlike-automation

echo.
echo 🚀 Para publicar no PyPI principal:
echo    twine upload dist/*

echo.
echo ✅ Build concluído! Use os comandos acima para publicar.
pause
