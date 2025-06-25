from typing import Dict, List, Any, Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage
import operator

from agents.lead_researcher import lead_researcher, create_research_plan, evaluate_research_progress, synthesize_research_results
from agents.search_subagent import run_subagent
from agents.citation_agent import citation_agent, process_documents_for_citations
from memory.research_memory import save_plan, retrieve_context, research_memory
from config import Config

class ResearchState(TypedDict):
    """Estado do workflow de pesquisa"""
    query: str
    research_plan: Dict[str, Any]
    subagent_results: Annotated[List[Dict], operator.add]
    current_iteration: int
    max_iterations: int
    research_complete: bool
    final_report: str
    cited_report: str
    sources: Annotated[List[Dict], operator.add]
    messages: Annotated[List[BaseMessage], operator.add]

class MultiAgentResearchWorkflow:
    """Workflow principal para pesquisa multi-agente"""
    
    def __init__(self):
        self.graph = None
        self._build_graph()
    
    def _build_graph(self):
        """Constrói o grafo do workflow"""
        
        # Define o grafo
        workflow = StateGraph(ResearchState)
        
        # Adiciona nós
        workflow.add_node("plan_research", self.plan_research)
        workflow.add_node("execute_subagents", self.execute_subagents)
        workflow.add_node("evaluate_progress", self.evaluate_progress)
        workflow.add_node("synthesize_results", self.synthesize_results)
        workflow.add_node("add_citations", self.add_citations)
        workflow.add_node("finalize_report", self.finalize_report)
        
        # Define entradas e saídas
        workflow.set_entry_point("plan_research")
        
        # Define transições
        workflow.add_edge("plan_research", "execute_subagents")
        workflow.add_edge("execute_subagents", "evaluate_progress")
        
        # Transição condicional para continuar ou finalizar pesquisa
        workflow.add_conditional_edges(
            "evaluate_progress",
            self.should_continue_research,
            {
                "continue": "execute_subagents",
                "synthesize": "synthesize_results"
            }
        )
        
        workflow.add_edge("synthesize_results", "add_citations")
        workflow.add_edge("add_citations", "finalize_report")
        workflow.add_edge("finalize_report", END)
        
        # Compila o grafo
        self.graph = workflow.compile()
    
    def plan_research(self, state: ResearchState) -> ResearchState:
        """Nó para planejamento da pesquisa"""
        
        print(f"📋 Planejando pesquisa para: {state['query']}")
        
        # Cria plano de pesquisa
        plan = lead_researcher.analyze_query(state["query"])
        
        # Atualiza estado
        state["research_plan"] = plan
        state["current_iteration"] = 0
        state["max_iterations"] = min(len(plan.get("subagent_tasks", [])) * 2, 6)
        state["research_complete"] = False
        
        print(f"✅ Plano criado com {len(plan.get('subagent_tasks', []))} tarefas")
        
        return state
    
    def execute_subagents(self, state: ResearchState) -> ResearchState:
        """Nó para execução de subagentes"""
        
        print(f"🤖 Executando subagentes (iteração {state['current_iteration'] + 1})")
        
        plan = state["research_plan"]
        current_iteration = state["current_iteration"]
        
        # Determina quais subagentes executar nesta iteração
        subagent_tasks = plan.get("subagent_tasks", [])
        
        new_results = []
        new_sources = []
        
        # Executa subagentes em paralelo (simulado sequencialmente)
        for i, task in enumerate(subagent_tasks):
            if current_iteration == 0 or i % 2 == current_iteration % 2:
                print(f"   🔍 Executando {task['id']}: {task['task']}")
                
                try:
                    result = run_subagent(
                        agent_id=task["id"],
                        task=task["task"],
                        focus=task.get("focus", "general")
                    )
                    
                    new_results.append(result)
                    new_sources.extend(result.get("sources", []))
                    
                except Exception as e:
                    print(f"❌ Erro no subagente {task['id']}: {e}")
                    # Continua com outros subagentes
                    
        # Atualiza estado
        state["subagent_results"].extend(new_results)
        state["sources"].extend(new_sources)
        state["current_iteration"] += 1
        
        print(f"✅ Iteração concluída: {len(new_results)} novos resultados")
        
        return state
    
    def evaluate_progress(self, state: ResearchState) -> ResearchState:
        """Nó para avaliação do progresso"""
        
        print("🔍 Avaliando progresso da pesquisa...")
        
        current_results = state["subagent_results"]
        current_iteration = state["current_iteration"]
        max_iterations = state["max_iterations"]
        
        # Critérios para finalizar pesquisa
        should_continue = (
            current_iteration < max_iterations and
            len(current_results) < Config.MAX_SUBAGENTS * 2 and
            lead_researcher.should_continue_research(current_results)
        )
        
        state["research_complete"] = not should_continue
        
        total_sources = len(state["sources"])
        print(f"📊 Progresso: {len(current_results)} resultados, {total_sources} fontes")
        
        return state
    
    def should_continue_research(self, state: ResearchState) -> str:
        """Decide se deve continuar pesquisando ou sintetizar"""
        
        if state["research_complete"]:
            return "synthesize"
        else:
            return "continue"
    
    def synthesize_results(self, state: ResearchState) -> ResearchState:
        """Nó para síntese dos resultados"""
        
        print("🧠 Sintetizando resultados da pesquisa...")
        
        query = state["query"]
        subagent_results = state["subagent_results"]
        
        try:
            # Sintetiza resultados
            final_report = lead_researcher.synthesize_results(query, subagent_results)
            state["final_report"] = final_report
            
            print("✅ Síntese concluída")
            
        except Exception as e:
            print(f"❌ Erro na síntese: {e}")
            # Fallback: concatena resultados
            fallback_report = f"# Relatório de Pesquisa: {query}\n\n"
            for i, result in enumerate(subagent_results, 1):
                fallback_report += f"## Resultado {i}\n{result.get('summary', str(result))}\n\n"
            state["final_report"] = fallback_report
        
        return state
    
    def add_citations(self, state: ResearchState) -> ResearchState:
        """Nó para adição de citações"""
        
        print("📚 Adicionando citações ao relatório...")
        
        final_report = state["final_report"]
        sources = state["sources"]
        
        try:
            # Remove duplicatas das fontes
            unique_sources = []
            seen_urls = set()
            
            for source in sources:
                url = source.get("url", "")
                if url not in seen_urls:
                    unique_sources.append(source)
                    seen_urls.add(url)
            
            # Adiciona citações
            cited_report = citation_agent.process_research_report(final_report, unique_sources)
            state["cited_report"] = cited_report
            
            print(f"✅ Citações adicionadas: {len(unique_sources)} fontes")
            
        except Exception as e:
            print(f"❌ Erro ao adicionar citações: {e}")
            # Fallback: usa relatório sem citações
            state["cited_report"] = final_report + "\n\n## Sources\n" + "\n".join(
                f"- {source.get('title', 'Untitled')}: {source.get('url', '')}"
                for source in sources[:10]
            )
        
        return state
    
    def finalize_report(self, state: ResearchState) -> ResearchState:
        """Nó para finalização do relatório"""
        
        print("📝 Finalizando relatório...")
        
        # Adiciona metadados ao relatório final
        cited_report = state["cited_report"]
        
        metadata = f"""
---
**Relatório de Pesquisa Multi-Agente**
- Query: {state['query']}
- Subagentes executados: {len(state['subagent_results'])}
- Fontes consultadas: {len(state['sources'])}
- Iterações: {state['current_iteration']}
---

{cited_report}
        """.strip()
        
        state["cited_report"] = metadata
        
        # Persiste resultados na memória
        research_memory.update_context("final_report", metadata)
        research_memory.update_context("research_completed", True)
        
        print("✅ Relatório finalizado!")
        
        return state
    
    def run_research(self, query: str) -> Dict[str, Any]:
        """Executa o workflow completo de pesquisa"""
        
        print(f"\n🚀 Iniciando pesquisa multi-agente")
        print(f"Query: {query}")
        print("=" * 50)
        
        # Estado inicial
        initial_state = {
            "query": query,
            "research_plan": {},
            "subagent_results": [],
            "current_iteration": 0,
            "max_iterations": 6,
            "research_complete": False,
            "final_report": "",
            "cited_report": "",
            "sources": [],
            "messages": []
        }
        
        try:
            # Executa workflow
            final_state = self.graph.invoke(initial_state)
            
            print("=" * 50)
            print("✅ Pesquisa concluída com sucesso!")
            
            return {
                "success": True,
                "query": query,
                "final_report": final_state["cited_report"],
                "sources": final_state["sources"],
                "subagent_results": final_state["subagent_results"],
                "metadata": {
                    "iterations": final_state["current_iteration"],
                    "num_sources": len(final_state["sources"]),
                    "num_subagents": len(final_state["subagent_results"])
                }
            }
            
        except Exception as e:
            print(f"❌ Erro na execução do workflow: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query,
                "final_report": f"Erro na pesquisa: {e}",
                "sources": [],
                "subagent_results": [],
                "metadata": {}
            }

# Instância global do workflow
research_workflow = MultiAgentResearchWorkflow()