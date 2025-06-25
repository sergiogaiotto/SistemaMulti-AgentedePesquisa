from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from config import Config
from tools.web_search import search_web, search_companies
from memory.research_memory import save_plan, retrieve_context, add_research_result, update_memory_context

class LeadResearcher:
    """Agente líder que coordena todo o processo de pesquisa"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=Config.MODEL_NAME,
            temperature=Config.TEMPERATURE,
            api_key=Config.OPENAI_API_KEY
        )
        self.subagents_created = 0
        self.research_complete = False
        
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """Analisa a query do usuário e cria plano de pesquisa"""
        
        system_prompt = """Você é um Lead Researcher especializado em coordenar pesquisas complexas.
        
        Sua tarefa é analisar a query do usuário e criar um plano de pesquisa detalhado.
        
        Para cada query, você deve:
        1. Identificar os aspectos principais que precisam ser pesquisados
        2. Determinar quantos subagentes são necessários (máximo 3)
        3. Definir tarefas específicas para cada subagente
        4. Criar uma estratégia de síntese dos resultados
        
        Responda em formato JSON com:
        {
            "analysis": "análise da query",
            "research_aspects": ["aspecto 1", "aspecto 2", ...],
            "subagent_tasks": [
                {"id": "subagent_1", "task": "tarefa específica", "focus": "foco da pesquisa"},
                ...
            ],
            "synthesis_strategy": "como combinar os resultados"
        }
        """
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Query: {query}")
            ]
            
            response = self.llm.invoke(messages)
            
            # Parse da resposta JSON
            import json
            try:
                plan_dict = json.loads(response.content)
            except json.JSONDecodeError:
                # Fallback se não conseguir parsear JSON
                plan_dict = {
                    "analysis": response.content,
                    "research_aspects": ["general research"],
                    "subagent_tasks": [{"id": "subagent_1", "task": query, "focus": "general"}],
                    "synthesis_strategy": "combine all results"
                }
            
            # Salva o plano na memória
            plan_text = json.dumps(plan_dict, indent=2, ensure_ascii=False)
            save_plan(plan_text, query)
            
            return plan_dict
            
        except Exception as e:
            print(f"Erro na análise da query: {e}")
            # Retorna plano básico em caso de erro
            return {
                "analysis": f"Pesquisa sobre: {query}",
                "research_aspects": ["general research"],
                "subagent_tasks": [{"id": "subagent_1", "task": query, "focus": "general"}],
                "synthesis_strategy": "combine results"
            }
    
    def should_continue_research(self, current_results: List[Dict]) -> bool:
        """Decide se deve continuar pesquisando ou finalizar"""
        
        if not current_results:
            return True  # Continua se não há resultados
        
        if len(current_results) >= Config.MAX_SUBAGENTS:
            return False  # Para se já tem muitos resultados
        
        # Analisa qualidade dos resultados atuais
        total_sources = sum(len(result.get("sources", [])) for result in current_results)
        
        if total_sources < 5:
            return True  # Continua se poucos fontes
        
        return False  # Para se tem resultados suficientes
    
    def synthesize_results(self, query: str, subagent_results: List[Dict]) -> str:
        """Sintetiza todos os resultados dos subagentes em um relatório final"""
        
        context = retrieve_context()
        
        system_prompt = """Você é um especialista em síntese de pesquisa.
        
        Sua tarefa é combinar os resultados de múltiplos subagentes em um relatório coeso e abrangente.
        
        Regras para o relatório:
        1. Comece com um resumo executivo
        2. Organize as informações por temas/categorias
        3. Mantenha consistência e evite repetições
        4. Cite fatos específicos que precisarão de referências
        5. Use formatação markdown para melhor legibilidade
        6. Termine com conclusões e insights
        
        Para consultas sobre empresas, inclua:
        - Nome da empresa
        - Website (se disponível)
        - Descrição do produto/serviço
        - Setor/indústria
        - Localização
        - Informações relevantes adicionais
        """
        
        # Prepara contexto para síntese
        synthesis_context = f"""
        Query original: {query}
        
        Plano de pesquisa: {context.get('plan', 'N/A')}
        
        Resultados dos subagentes:
        """
        
        for i, result in enumerate(subagent_results, 1):
            synthesis_context += f"\n\nSubagente {i}:\n{result.get('summary', str(result))}"
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=synthesis_context)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            print(f"Erro na síntese: {e}")
            # Fallback: concatena resultados simples
            fallback_report = f"# Relatório de Pesquisa: {query}\n\n"
            for i, result in enumerate(subagent_results, 1):
                fallback_report += f"## Resultado {i}\n{result.get('summary', str(result))}\n\n"
            return fallback_report
    
    def coordinate_research(self, query: str) -> Dict[str, Any]:
        """Coordena todo o processo de pesquisa"""
        
        print(f"🎯 Iniciando pesquisa: {query}")
        
        # 1. Analisa query e cria plano
        plan = self.analyze_query(query)
        print(f"📋 Plano criado com {len(plan['subagent_tasks'])} subagentes")
        
        # 2. Coordena execução dos subagentes
        subagent_results = []
        
        for task in plan["subagent_tasks"]:
            print(f"🔍 Executando {task['id']}: {task['task']}")
            
            # Simula execução do subagente (será implementado no workflow)
            result = {
                "agent_id": task["id"],
                "task": task["task"],
                "status": "completed",
                "summary": f"Resultado para: {task['task']}",
                "sources": []
            }
            
            subagent_results.append(result)
            add_research_result(task["id"], result)
        
        # 3. Sintetiza resultados
        final_report = self.synthesize_results(query, subagent_results)
        
        return {
            "query": query,
            "plan": plan,
            "subagent_results": subagent_results,
            "final_report": final_report,
            "status": "completed"
        }

# Instância global do agente
lead_researcher = LeadResearcher()

@tool
def create_research_plan(query: str) -> Dict:
    """
    Cria um plano de pesquisa detalhado para a query.
    
    Args:
        query: Query do usuário
        
    Returns:
        Plano de pesquisa estruturado
    """
    return lead_researcher.analyze_query(query)

@tool
def evaluate_research_progress(current_results: List[Dict]) -> bool:
    """
    Avalia se a pesquisa deve continuar ou finalizar.
    
    Args:
        current_results: Resultados atuais dos subagentes
        
    Returns:
        True se deve continuar, False se deve finalizar
    """
    return lead_researcher.should_continue_research(current_results)

@tool
def synthesize_research_results(query: str, results: List[Dict]) -> str:
    """
    Sintetiza todos os resultados em um relatório final.
    
    Args:
        query: Query original
        results: Lista de resultados dos subagentes
        
    Returns:
        Relatório final sintetizado
    """
    return lead_researcher.synthesize_results(query, results)

@tool
def complete_task(result: Dict) -> Dict:
    """
    Marca uma tarefa como completa e retorna resultado.
    
    Args:
        result: Resultado da tarefa
        
    Returns:
        Resultado processado
    """
    result["completed_at"] = __import__("datetime").datetime.now().isoformat()
    result["status"] = "completed"
    return result