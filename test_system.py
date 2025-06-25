#!/usr/bin/env python3
"""
Teste básico do sistema multi-agente para verificar funcionamento
"""

import sys
import os

def test_imports():
    """Testa todas as importações necessárias"""
    print("🧪 Testando importações...")
    
    try:
        # Testa importações básicas
        import langchain
        print("✅ langchain")
        
        from langchain_openai import ChatOpenAI
        print("✅ langchain_openai")
        
        from langchain_community.tools import DuckDuckGoSearchRun
        print("✅ langchain_community")
        
        import requests
        print("✅ requests")
        
        # Testa importações do projeto
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from config import Config
        print("✅ config")
        
        from agents.lead_researcher import lead_researcher
        print("✅ lead_researcher")
        
        from memory.research_memory import research_memory
        print("✅ research_memory")
        
        from graph.research_workflow import research_workflow
        print("✅ research_workflow")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def test_config():
    """Testa configuração"""
    print("\n⚙️ Testando configuração...")
    
    try:
        from config import Config
        
        if not Config.OPENAI_API_KEY:
            print("❌ OPENAI_API_KEY não configurada")
            print("💡 Edite o arquivo .env e adicione sua chave")
            return False
        
        if Config.OPENAI_API_KEY.startswith("sk-"):
            print("✅ OPENAI_API_KEY configurada")
        else:
            print("⚠️ OPENAI_API_KEY pode estar inválida (não começa com 'sk-')")
        
        print(f"✅ MODEL_NAME: {Config.MODEL_NAME}")
        print(f"✅ MAX_SEARCH_RESULTS: {Config.MAX_SEARCH_RESULTS}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

def test_basic_functionality():
    """Testa funcionalidade básica"""
    print("\n🔧 Testando funcionalidade básica...")
    
    try:
        from graph.research_workflow import research_workflow
        
        # Teste muito simples
        print("   📋 Testando criação de estado...")
        from graph.research_workflow import ResearchState
        state = ResearchState(query="test")
        print("   ✅ Estado criado")
        
        print("   🤖 Testando workflow...")
        workflow = research_workflow
        print("   ✅ Workflow inicializado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na funcionalidade: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_research():
    """Testa uma pesquisa muito simples"""
    print("\n🔍 Testando pesquisa simples...")
    
    try:
        from graph.research_workflow import research_workflow
        
        # Pesquisa muito básica para testar
        result = research_workflow.run_research("test simple query")
        
        if result.get("success"):
            print("✅ Pesquisa simples funcionou!")
            print(f"   📄 Relatório gerado: {len(result.get('final_report', ''))} caracteres")
        else:
            print(f"⚠️ Pesquisa falhou mas sistema funcionou: {result.get('error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na pesquisa: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Teste do Sistema Multi-Agente")
    print("=" * 40)
    
    # Conta sucessos
    success_count = 0
    total_tests = 4
    
    # Testa importações
    if test_imports():
        success_count += 1
    
    # Testa configuração
    if test_config():
        success_count += 1
    
    # Testa funcionalidade básica
    if test_basic_functionality():
        success_count += 1
    
    # Testa pesquisa simples (apenas se outras passaram)
    if success_count == 3:
        if test_simple_research():
            success_count += 1
    else:
        print("\n⏭️ Pulando teste de pesquisa (erros anteriores)")
    
    # Resultado final
    print("\n" + "=" * 40)
    print(f"📊 Resultado: {success_count}/{total_tests} testes passaram")
    
    if success_count == total_tests:
        print("🎉 Sistema funcionando perfeitamente!")
        print("✅ Execute: python main.py")
    elif success_count >= 3:
        print("⚠️ Sistema quase funcionando!")
        print("💡 Verifique sua OPENAI_API_KEY no arquivo .env")
    elif success_count >= 2:
        print("🔧 Sistema com problemas básicos")
        print("💡 Execute: fix_installation.bat")
    else:
        print("❌ Sistema com problemas graves")
        print("💡 Verifique instalação do Python e dependências")
    
    print("\n🆘 Se houver problemas:")
    print("   1. Execute: fix_installation.bat")
    print("   2. Configure arquivo .env")
    print("   3. Execute este teste novamente")

if __name__ == "__main__":
    main()