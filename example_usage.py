#!/usr/bin/env python3
"""
Exemplos de uso do Sistema Multi-Agente de Pesquisa

Este arquivo demonstra diferentes formas de usar o sistema programaticamente.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config
from graph.research_workflow import research_workflow
from utils.helpers import generate_research_summary, save_research_to_file

def example_basic_research():
    """Exemplo básico de pesquisa"""
    
    print("🔍 Exemplo 1: Pesquisa Básica")
    print("=" * 50)
    
    query = "Quais as top empresas de 2025?"
    
    try:
        result = research_workflow.run_research(query)
        
        if result["success"]:
            print("✅ Pesquisa bem-sucedida!")
            print(f"Relatório:\n{result['final_report'][:500]}...")
        else:
            print(f"❌ Erro: {result['error']}")
            
    except Exception as e:
        print(f"❌ Erro na execução: {e}")

def example_company_research():
    """Exemplo de pesquisa específica sobre empresas"""
    
    print("\n🏢 Exemplo 2: Pesquisa de Empresas")
    print("=" * 50)
    
    query = """Encontre empresas que trabalham com veículos autônomos nos EUA.
            Para cada empresa, inclua:
            - Nome e site da empresa
            - Produto/serviço principal
            - Localização da sede
            - Parcerias ou financiamentos recentes"""
                
    try:
        result = research_workflow.run_research(query)
        
        if result["success"]:
            # Salva automaticamente o resultado
            filename = save_research_to_file(result, "resultado_pesquisa_veiculos_autonomos.txt")
            print(f"✅ Relatório salvo em: {filename}")
            
            # Mostra estatísticas
            metadata = result.get("metadata", {})
            print(f"📊 Estatísticas:")
            print(f"   • Subagentes: {metadata.get('num_subagents', 0)}")
            print(f"   • Fontes: {metadata.get('num_sources', 0)}")
            print(f"   • Iterações: {metadata.get('iterations', 0)}")
        else:
            print(f"❌ Erro: {result['error']}")
            
    except Exception as e:
        print(f"❌ Erro na execução: {e}")

def example_programmatic_usage():
    """Exemplo de uso programático avançado"""
    
    print("\n⚙️ Exemplo 3: Uso Programático")
    print("=" * 50)
    
    # Lista de queries para processar
    queries = [
                "As 3 principais startups de computação quântica",
                "Empresas desenvolvendo interfaces cérebro-computador",
                "Parcerias mais recentes no setor de energia renovável"    ]
    
    results = []
    
    for i, query in enumerate(queries, 1):
        print(f"\n🔄 Processando query {i}/{len(queries)}: {query}")
        
        try:
            result = research_workflow.run_research(query)
            results.append(result)
            
            if result["success"]:
                print(f"   ✅ Concluída - {len(result.get('sources', []))} fontes")
            else:
                print(f"   ❌ Erro: {result.get('error', 'Desconhecido')}")
                
        except Exception as e:
            print(f"   ❌ Exceção: {e}")
            results.append({
                "success": False,
                "error": str(e),
                "query": query
            })
    
    # Resumo final
    successful = sum(1 for r in results if r.get("success"))
    print(f"\n📈 Resumo: {successful}/{len(queries)} pesquisas bem-sucedidas")
    
    return results

def example_with_custom_config():
    """Exemplo usando configurações customizadas"""
    
    print("\n⚙️ Exemplo 4: Configurações Customizadas")
    print("=" * 50)
    
    # Modifica temporariamente configurações
    original_max_results = Config.MAX_SEARCH_RESULTS
    original_max_subagents = Config.MAX_SUBAGENTS
    
    try:
        # Configurações para pesquisa mais rápida
        Config.MAX_SEARCH_RESULTS = 5
        Config.MAX_SUBAGENTS = 2
        
        query = "Latest developments in electric aircraft"
        
        result = research_workflow.run_research(query)
        
        if result["success"]:
            print("✅ Pesquisa rápida concluída!")
            print(generate_research_summary(result))
        else:
            print(f"❌ Erro: {result['error']}")
            
    finally:
        # Restaura configurações originais
        Config.MAX_SEARCH_RESULTS = original_max_results
        Config.MAX_SUBAGENTS = original_max_subagents

def example_error_handling():
    """Exemplo de tratamento de erros"""
    
    print("\n🛡️ Exemplo 5: Tratamento de Erros")
    print("=" * 50)
    
    # Query que pode causar problemas
    problematic_query = ""  # Query vazia
    
    try:
        result = research_workflow.run_research(problematic_query)
        
        if not result["success"]:
            print(f"❌ Pesquisa falhou como esperado: {result['error']}")
            
            # Estratégias de recuperação
            fallback_query = "general AI research trends 2025"
            print(f"🔄 Tentando query de fallback: {fallback_query}")
            
            fallback_result = research_workflow.run_research(fallback_query)
            
            if fallback_result["success"]:
                print("✅ Fallback bem-sucedido!")
            else:
                print(f"❌ Fallback também falhou: {fallback_result['error']}")
        else:
            print("⚠️ Query vazia funcionou inesperadamente")
            
    except Exception as e:
        print(f"❌ Exceção capturada: {e}")
        print("🔧 Isso é esperado para demonstrar tratamento de erros")

def main():
    """Executa todos os exemplos"""
    
    print("🚀 Exemplos de Uso - Sistema Multi-Agente")
    print("=" * 60)
    
    try:
        # Valida configuração
        Config.validate()
        
        # Executa exemplos
        example_basic_research()
        example_company_research()
        example_programmatic_usage()
        example_with_custom_config()
        example_error_handling()
        
        print("\n🎉 Todos os exemplos foram executados!")
        print("✨ Explore o código para entender como funciona cada exemplo")
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        print("💡 Verifique seu arquivo .env e configurações")

if __name__ == "__main__":
    main()