#!/usr/bin/env python3
"""
Sistema Multi-Agente de Pesquisa Simplificado
Versão autônoma sem dependências complexas
"""

import os
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Any
import openai
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    """Configurações simplificadas"""
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
    MAX_SUBAGENTS = int(os.getenv("MAX_SUBAGENTS", "3"))

class SimpleWebSearch:
    """Pesquisa web simples usando DuckDuckGo"""
    
    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """Executa pesquisa web simples"""
        try:
            # Simula pesquisa web - em ambiente real, pode usar APIs específicas
            print(f"   🔍 Pesquisando: {query}")
            
            # Resultados simulados para demonstração
            results = [
                {
                    "title": f"Resultado 1 para: {query}",
                    "url": f"https://example.com/1?q={query.replace(' ', '+')}",
                    "content": f"Informações relevantes sobre {query}. Este é um resultado simulado que contém informações úteis para a pesquisa.",
                    "score": 0.9
                },
                {
                    "title": f"Artigo sobre {query}",
                    "url": f"https://example.com/2?q={query.replace(' ', '+')}",
                    "content": f"Análise detalhada de {query}. Dados atualizados e informações precisas sobre o tópico pesquisado.",
                    "score": 0.8
                },
                {
                    "title": f"Guia completo: {query}",
                    "url": f"https://example.com/3?q={query.replace(' ', '+')}",
                    "content": f"Guia abrangente sobre {query} com exemplos práticos e casos de uso reais.",
                    "score": 0.7
                }
            ]
            
            time.sleep(1)  # Simula tempo de pesquisa
            return results[:num_results]
            
        except Exception as e:
            print(f"Erro na pesquisa: {e}")
            return []

class SimpleAgent:
    """Agente simplificado usando OpenAI diretamente"""
    
    def __init__(self, agent_id: str, role: str):
        self.agent_id = agent_id
        self.role = role
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.search_tool = SimpleWebSearch()
    
    def execute_task(self, task: str, context: str = "") -> Dict[str, Any]:
        """Executa uma tarefa específica"""
        
        system_prompt = f"""Você é um {self.role} especializado em pesquisa.
        
        Sua tarefa: {task}
        
        Contexto adicional: {context}
        
        Instruções:
        1. Analise a tarefa cuidadosamente
        2. Execute pesquisas se necessário
        3. Forneça resultados estruturados e úteis
        4. Seja preciso e objetivo
        
        Responda em formato JSON:
        {{
            "analysis": "sua análise da tarefa",
            "findings": ["descoberta 1", "descoberta 2", ...],
            "summary": "resumo dos resultados",
            "next_steps": ["próximo passo 1", "próximo passo 2", ...]
        }}
        """
        
        try:
            # Executa pesquisa se necessário
            search_results = []
            if "pesquis" in task.lower() or "find" in task.lower() or "list" in task.lower():
                search_results = self.search_tool.search(task, Config.MAX_SEARCH_RESULTS)
            
            # Adiciona resultados de pesquisa ao contexto
            if search_results:
                context += "\n\nResultados da pesquisa:\n"
                for i, result in enumerate(search_results, 1):
                    context += f"{i}. {result['title']}\n   {result['content'][:200]}...\n\n"
            
            # Chama OpenAI
            response = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Tarefa: {task}\n\nContexto: {context}"}
                ],
                temperature=0.1
            )
            
            result_text = response.choices[0].message.content
            
            # Tenta parsear JSON, senão retorna resultado simples
            try:
                result_json = json.loads(result_text)
            except:
                result_json = {
                    "analysis": result_text,
                    "findings": [result_text],
                    "summary": result_text,
                    "next_steps": []
                }
            
            return {
                "agent_id": self.agent_id,
                "task": task,
                "result": result_json,
                "sources": search_results,
                "status": "completed"
            }
            
        except Exception as e:
            print(f"Erro no agente {self.agent_id}: {e}")
            return {
                "agent_id": self.agent_id,
                "task": task,
                "result": {"error": str(e)},
                "sources": [],
                "status": "error"
            }

class SimpleMultiAgentSystem:
    """Sistema multi-agente simplificado"""
    
    def __init__(self):
        self.agents = {}
        self.memory = {
            "query": "",
            "plan": {},
            "results": [],
            "final_report": ""
        }
    
    def create_agent(self, agent_id: str, role: str) -> SimpleAgent:
        """Cria um novo agente"""
        agent = SimpleAgent(agent_id, role)
        self.agents[agent_id] = agent
        return agent
    
    def run_research(self, query: str) -> Dict[str, Any]:
        """Executa pesquisa multi-agente completa"""
        
        print(f"\n🚀 Sistema Multi-Agente Iniciado")
        print(f"Query: {query}")
        print("=" * 50)
        
        start_time = time.time()
        
        try:
            # 1. Planejamento
            print("📋 Fase 1: Planejamento")
            lead_agent = self.create_agent("lead_researcher", "Pesquisador Líder")
            
            plan_task = f"Analise esta consulta e crie um plano de pesquisa: {query}"
            plan_result = lead_agent.execute_task(plan_task)
            self.memory["plan"] = plan_result["result"]
            
            print(f"   ✅ Plano criado pelo {plan_result['agent_id']}")
            
            # 2. Execução de Subagentes
            print("\n🤖 Fase 2: Execução de Subagentes")
            
            # Cria subagentes especializados
            subagents = [
                ("researcher_1", "Pesquisador de Empresas", f"Encontre empresas relacionadas a: {query}"),
                ("researcher_2", "Analista de Mercado", f"Analise tendências e dados sobre: {query}"),
                ("researcher_3", "Especialista em Tecnologia", f"Pesquise aspectos técnicos de: {query}")
            ]
            
            all_results = []
            all_sources = []
            
            for agent_id, role, task in subagents[:Config.MAX_SUBAGENTS]:
                print(f"   🔍 Executando {agent_id}: {role}")
                
                agent = self.create_agent(agent_id, role)
                result = agent.execute_task(task, str(self.memory["plan"]))
                
                all_results.append(result)
                all_sources.extend(result.get("sources", []))
                
                if result["status"] == "completed":
                    print(f"      ✅ Concluído: {len(result.get('sources', []))} fontes")
                else:
                    print(f"      ⚠️ Erro: {result['result'].get('error', 'Desconhecido')}")
            
            self.memory["results"] = all_results
            
            # 3. Síntese
            print("\n🧠 Fase 3: Síntese dos Resultados")
            
            synthesis_context = f"""
            Query original: {query}
            
            Plano de pesquisa: {json.dumps(self.memory['plan'], indent=2)}
            
            Resultados dos agentes:
            """
            
            for result in all_results:
                synthesis_context += f"\n{result['agent_id']}: {json.dumps(result['result'], indent=2)}\n"
            
            synthesis_task = f"Sintetize todos os resultados em um relatório final sobre: {query}"
            synthesis_agent = self.create_agent("synthesizer", "Sintetizador de Resultados")
            final_result = synthesis_agent.execute_task(synthesis_task, synthesis_context)
            
            # 4. Relatório Final
            print("\n📝 Fase 4: Geração do Relatório Final")
            
            report = self._generate_final_report(query, all_results, final_result, all_sources)
            self.memory["final_report"] = report
            
            elapsed_time = time.time() - start_time
            
            print("=" * 50)
            print(f"✅ Pesquisa concluída em {elapsed_time:.1f} segundos")
            
            return {
                "success": True,
                "query": query,
                "final_report": report,
                "sources": all_sources,
                "subagent_results": all_results,
                "metadata": {
                    "execution_time": elapsed_time,
                    "num_sources": len(all_sources),
                    "num_subagents": len(all_results)
                }
            }
            
        except Exception as e:
            print(f"❌ Erro na execução: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "final_report": f"Erro na pesquisa: {e}",
                "sources": [],
                "subagent_results": [],
                "metadata": {}
            }
    
    def _generate_final_report(self, query: str, results: List[Dict], synthesis: Dict, sources: List[Dict]) -> str:
        """Gera relatório final formatado"""
        
        timestamp = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        
        report = f"""# Relatório de Pesquisa Multi-Agente

**Query:** {query}
**Gerado em:** {timestamp}
**Agentes executados:** {len(results)}
**Fontes consultadas:** {len(sources)}

---

## Resumo Executivo

{synthesis['result'].get('summary', 'Resumo não disponível')}

## Principais Descobertas

"""
        
        # Adiciona descobertas dos agentes
        for i, result in enumerate(results, 1):
            if result['status'] == 'completed':
                agent_findings = result['result'].get('findings', [])
                if agent_findings:
                    report += f"\n### {result['agent_id']}\n"
                    for finding in agent_findings:
                        report += f"- {finding}\n"
        
        # Adiciona análise final
        if synthesis['result'].get('analysis'):
            report += f"\n## Análise Detalhada\n\n{synthesis['result']['analysis']}\n"
        
        # Adiciona fontes
        if sources:
            report += "\n## Fontes Consultadas\n\n"
            for i, source in enumerate(sources, 1):
                report += f"[{i}] {source['title']} - {source['url']}\n"
        
        # Adiciona próximos passos
        next_steps = synthesis['result'].get('next_steps', [])
        if next_steps:
            report += "\n## Próximos Passos Recomendados\n\n"
            for step in next_steps:
                report += f"- {step}\n"
        
        return report

def main():
    """Função principal"""
    
    print("🔬 Sistema Multi-Agente de Pesquisa Simplificado")
    print("=" * 50)
    
    # Verifica configuração
    if not Config.OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY não configurada!")
        print("📝 Crie um arquivo .env com:")
        print("OPENAI_API_KEY=sk-sua_chave_aqui")
        return
    
    if not Config.OPENAI_API_KEY.startswith("sk-"):
        print("⚠️ OPENAI_API_KEY pode estar inválida")
    
    print("✅ Configuração OK")
    
    # Menu interativo
    while True:
        print("\n🎯 MENU")
        print("1. 🔍 Executar Pesquisa")
        print("2. 🎮 Demonstração")
        print("3. 🚪 Sair")
        
        choice = input("\nEscolha (1-3): ").strip()
        
        if choice == "1":
            query = input("\n📝 Digite sua pesquisa: ").strip()
            if query:
                system = SimpleMultiAgentSystem()
                result = system.run_research(query)
                
                print("\n" + "="*60)
                print("📄 RELATÓRIO FINAL")
                print("="*60)
                print(result["final_report"])
                
                save = input("\n💾 Salvar relatório? (s/N): ").strip().lower()
                if save in ['s', 'sim', 'y', 'yes']:
                    filename = f"research_{int(time.time())}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(result["final_report"])
                    print(f"✅ Salvo em: {filename}")
        
        elif choice == "2":
            print("\n🎮 Demonstração")
            demo_query = "Top 5 AI companies working on agents in 2025"
            print(f"Executando: {demo_query}")
            
            system = SimpleMultiAgentSystem()
            result = system.run_research(demo_query)
            
            print("\n📊 Resultado da Demonstração:")
            print(f"✅ Sucesso: {result['success']}")
            print(f"📄 Relatório: {len(result['final_report'])} caracteres")
            print(f"📚 Fontes: {result['metadata'].get('num_sources', 0)}")
        
        elif choice == "3":
            print("\n👋 Obrigado por usar o Sistema Multi-Agente!")
            break
        
        else:
            print("❌ Opção inválida")

if __name__ == "__main__":
    main()