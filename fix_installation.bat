@echo off
chcp 65001 > nul
echo.
echo 🔧 Corrigindo instalação do Sistema Multi-Agente
echo ===============================================
echo.

echo ⚠️  Desinstalando versões incompatíveis...
pip uninstall langgraph langchain langchain-openai langchain-community -y

echo.
echo 📦 Instalando versões compatíveis...
pip install langchain==0.2.16
pip install langchain-openai==0.1.25
pip install langchain-community==0.2.16
pip install langgraph==0.1.19
pip install requests beautifulsoup4 python-dotenv tavily-python pydantic typing-extensions

echo.
echo 🧪 Testando instalação...
python -c "print('Testando importações...')"
python -c "from langchain_openai import ChatOpenAI; print('✅ langchain-openai OK')"
python -c "from langchain_community.tools import DuckDuckGoSearchRun; print('✅ langchain-community OK')"
python -c "import requests; print('✅ requests OK')"
python -c "from config import Config; print('✅ config OK')"

echo.
echo 🎯 Testando componentes principais...
python -c "from agents.lead_researcher import lead_researcher; print('✅ lead_researcher OK')"
python -c "from memory.research_memory import research_memory; print('✅ research_memory OK')"
python -c "from graph.research_workflow import research_workflow; print('✅ research_workflow OK')"

echo.
echo ✅ Correção concluída!
echo.
echo 💡 Agora execute: python main.py
echo.
pause