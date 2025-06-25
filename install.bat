@echo off
chcp 65001 > nul
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        🔬 Sistema Multi-Agente de Pesquisa Avançada         ║
echo ║                     Instalação Automática                   ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo ⚡ Verificando Python...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo 📥 Baixe Python 3.8+ de: https://www.python.org/downloads/
    echo ⚠️  Marque "Add Python to PATH" durante a instalação
    pause
    exit /b 1
) else (
    echo ✅ Python encontrado
)

echo.
echo 📦 Instalando dependências...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erro na instalação das dependências
    echo 💡 Tente executar: pip install --upgrade pip
    pause
    exit /b 1
) else (
    echo ✅ Dependências instaladas
)

echo.
echo ⚙️ Configurando arquivo de ambiente...
if not exist .env (
    copy .env.example .env > nul
    echo ✅ Arquivo .env criado
    echo.
    echo ⚠️  IMPORTANTE: Edite o arquivo .env com suas chaves de API
    echo    📝 Abra .env e adicione sua OPENAI_API_KEY
    echo.
    pause
) else (
    echo ✅ Arquivo .env já existe
)

echo.
echo 🧪 Testando configuração...
python -c "from config import Config; Config.validate()" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Configuração incompleta
    echo    📝 Execute: notepad .env
    echo    🔑 Adicione sua OPENAI_API_KEY
) else (
    echo ✅ Configuração válida
)

echo.
echo 📁 Estrutura do projeto criada:
tree /F 2>nul || dir /s /b *.py

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ✅ INSTALAÇÃO CONCLUÍDA                   ║
echo ║                                                              ║
echo ║  Para iniciar o sistema:                                     ║
echo ║  1. Configure sua OPENAI_API_KEY no arquivo .env             ║
echo ║  2. Execute: python main.py                                  ║
echo ║                                                              ║
echo ║  Comandos úteis:                                             ║
echo ║  • python main.py         - Sistema completo                ║
echo ║  • python example_usage.py - Exemplos de uso                ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 Deseja executar o sistema agora? (s/N)
set /p choice=
if /i "%choice%"=="s" (
    echo.
    echo 🎯 Iniciando sistema...
    python main.py
) else (
    echo.
    echo 👋 Sistema instalado! Execute 'python main.py' quando estiver pronto.
)

pause