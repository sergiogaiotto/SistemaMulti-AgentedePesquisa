#!/usr/bin/env python3
"""
Sistema Multi-Agente de Pesquisa Avançada

Este sistema implementa uma arquitetura multi-agente usando LangGraph para 
coordenar pesquisas complexas com múltiplos agentes especializados.

Uso:
    python main.py
"""

import sys
import os
import time
from typing import Dict, Any

# Adiciona o diretório atual ao Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from graph.research_workflow import research_workflow
from utils.helpers import (
    format_elapsed_time, 
    print_research_status, 
    generate_research_summary,
    save_research_to_file,
    ResearchTimer
)

def print_banner():
    """Imprime banner do sistema"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🔬 Sistema Multi-Agente de Pesquisa Avançada         ║
║                                                              ║
║   Arquitetura orquestrador-trabalhador com LangGraph        ║
║   • Lead Researcher (Coordenador)                           ║
║   • Search Subagents (Pesquisadores Especializados)         ║
║   • Citation Agent (Processador de Citações)                ║
║   • Memory System (Persistência de Contexto)                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_interactive_mode():
    """Executa o sistema em modo interativo"""
    
    print("\n🎯 Modo Interativo Iniciado")
    print("Digite 'quit', 'exit' ou 'sair' para encerrar\n")
    
    while True:
        try:
            # Solicita query do usuário
            query = input("📝 Digite sua pesquisa: ").strip()
            
            # Verifica comandos de saída
            if query.lower() in ['quit', 'exit', 'sair', '']:
                print("\n👋 Encerrando sistema. Até logo!")
                break
            
            # Executa pesquisa
            result = execute_research(query)
            
            # Mostra resultados
            display_results(result)
            
            # Pergunta se quer salvar
            save_prompt = input("\n💾 Deseja salvar o relatório em arquivo? (s/N): ").strip().lower()
            if save_prompt in ['s', 'sim', 'y', 'yes']:
                filename = save_research_to_file(result)
                if filename:
                    print(f"✅ Relatório salvo em: {filename}")
            
            print("\n" + "="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Operação cancelada pelo usuário")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
            print("Continuando...")

def execute_research(query: str) -> Dict[str, Any]:
    """Executa uma pesquisa completa"""
    
    timer = ResearchTimer()
    timer.mark_step("início")
    
    print_research_status("🚀 Iniciando pesquisa", f"Query: {query}")
    
    try:
        # Executa workflow de pesquisa
        timer.mark_step("execução_workflow")
        result = research_workflow.run_research(query)
        timer.mark_step("fim_workflow")
        
        # Adiciona informações de timing
        result["timing"] = {
            "total_duration": timer.get_total_elapsed(),
            "workflow_duration": timer.get_step_duration("fim_workflow", "execução_workflow")
        }
        
        if result.get("success"):
            print_research_status("✅ Pesquisa concluída com sucesso!")
        else:
            print_research_status("❌ Pesquisa falhou", result.get("error", "Erro desconhecido"))
        
        # Imprime relatório de timing
        timer.print_timing_report()
        
        return result
        
    except Exception as e:
        print_research_status("❌ Erro durante execução", str(e))
        return {
            "success": False,
            "error": str(e),
            "query": query,
            "final_report": f"Erro na pesquisa: {e}",
            "sources": [],
            "subagent_results": [],
            "metadata": {}
        }

def display_results(result: Dict[str, Any]):
    """Exibe resultados da pesquisa"""
    
    print("\n" + "="*60)
    print("📊 RESULTADOS DA PESQUISA")
    print("="*60)
    
    # Resumo executivo
    summary = generate_research_summary(result)
    print(summary)
    
    if result.get("success"):
        # Relatório principal
        print("\n📄 RELATÓRIO COMPLETO")
        print("-"*40)
        report = result.get("final_report", "Relatório não disponível")
        print(report)
        
        # Estatísticas
        metadata = result.get("metadata", {})
        timing = result.get("timing", {})
        
        print("\n📈 ESTATÍSTICAS")
        print("-"*25)
        print(f"• Subagentes executados: {metadata.get('num_subagents', 0)}")
        print(f"• Fontes consultadas: {metadata.get('num_sources', 0)}")
        print(f"• Iterações realizadas: {metadata.get('iterations', 0)}")
        
        if timing.get("total_duration"):
            print(f"• Tempo total: {format_elapsed_time(timing['total_duration'])}")
    
    print("="*60)

def run_demo_mode():
    """Executa demonstração com queries de exemplo"""
    
    demo_queries = [
        "What are all the companies in the United States working on AI agents in 2025? Make a list of at least 10 companies with name, website, product description, and industry.",
        "List the top 10 AI startups founded in 2024 with their funding information",
        "Find companies developing autonomous vehicles and their latest partnerships"
    ]
    
    print("\n🎮 Modo Demonstração")
    print("Executando queries de exemplo...\n")
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{'='*20} DEMO {i}/3 {'='*20}")
        print(f"Query: {query}")
        print("-"*60)
        
        result = execute_research(query)
        display_results(result)
        
        if i < len(demo_queries):
            input("\nPressione Enter para continuar...")

def main():
    """Função principal"""
    
    try:
        # Validar configurações
        Config.validate()
        
        # Mostrar banner
        print_banner()
        
        # Menu principal
        while True:
            print("\n🎯 MENU PRINCIPAL")
            print("-" * 30)
            print("1. 🔍 Modo Interativo")
            print("2. 🎮 Modo Demonstração")
            print("3. ⚙️  Testar Configurações")
            print("4. 📖 Ajuda")
            print("5. 🚪 Sair")
            
            choice = input("\nEscolha uma opção (1-5): ").strip()
            
            if choice == "1":
                run_interactive_mode()
            elif choice == "2":
                run_demo_mode()
            elif choice == "3":
                test_configuration()
            elif choice == "4":
                show_help()
            elif choice == "5":
                print("\n👋 Obrigado por usar o Sistema Multi-Agente!")
                break
            else:
                print("\n❌ Opção inválida. Tente novamente.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Sistema encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        print("Verifique suas configurações e tente novamente.")

def test_configuration():
    """Testa configurações do sistema"""
    
    print("\n🔧 Testando Configurações...")
    print("-" * 40)
    
    # Testa OpenAI
    try:
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(api_key=Config.OPENAI_API_KEY, model=Config.MODEL_NAME)
        response = llm.invoke("Test")
        print("✅ OpenAI API: Funcionando")
    except Exception as e:
        print(f"❌ OpenAI API: Erro - {e}")
    
    # Testa Tavily (opcional)
    if Config.TAVILY_API_KEY:
        try:
            from langchain_community.tools.tavily_search import TavilySearchResults
            search = TavilySearchResults(max_results=1)
            search.run("test")
            print("✅ Tavily API: Funcionando")
        except Exception as e:
            print(f"❌ Tavily API: Erro - {e}")
    else:
        print("⚠️  Tavily API: Não configurada (usando DuckDuckGo)")
    
    # Testa importações
    try:
        from graph.research_workflow import research_workflow
        print("✅ LangGraph: Funcionando")
    except Exception as e:
        print(f"❌ LangGraph: Erro - {e}")
    
    print("-" * 40)
    print("✅ Teste de configuração concluído!")

def show_help():
    """Mostra ajuda e documentação"""
    
    help_text = """
📖 AJUDA - Sistema Multi-Agente de Pesquisa

🎯 COMO USAR:
• Modo Interativo: Digite suas perguntas em linguagem natural
• Modo Demo: Veja exemplos de pesquisas complexas

💡 TIPOS DE PESQUISA SUPORTADOS:
• Pesquisa de empresas e startups
• Análise de mercado e tendências
• Informações técnicas e científicas
• Relatórios comparativos

🔧 CONFIGURAÇÃO:
• Edite o arquivo .env com suas chaves de API
• OpenAI API é obrigatória
• Tavily API é opcional (melhora qualidade)

📝 EXEMPLOS DE QUERIES:
• "List top 10 AI companies in Silicon Valley"
• "Find startups working on quantum computing"
• "Compare electric vehicle manufacturers"

⚙️ ARQUITETURA:
• Lead Researcher: Coordena todo o processo
• Search Subagents: Executam pesquisas especializadas
• Citation Agent: Adiciona citações aos relatórios
• Memory System: Mantém contexto da pesquisa

🆘 SUPORTE:
• Verifique configurações em .env
• Teste APIs no menu de configurações
• Consulte logs para detalhes de erros
    """
    
    print(help_text)

if __name__ == "__main__":
    main()