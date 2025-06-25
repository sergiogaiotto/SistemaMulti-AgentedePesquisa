import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from langchain_core.tools import tool
from config import Config

class ResearchMemory:
    """Sistema de memória para pesquisa multi-agente"""
    
    def __init__(self):
        self.memory = {
            "research_plan": None,
            "query": None,
            "subagent_results": [],
            "sources": [],
            "context": {},
            "metadata": {
                "created_at": None,
                "token_count": 0,
                "last_updated": None
            }
        }
    
    def save_research_plan(self, plan: str, query: str) -> bool:
        """Salva o plano de pesquisa na memória"""
        try:
            self.memory["research_plan"] = plan
            self.memory["query"] = query
            self.memory["metadata"]["created_at"] = datetime.now().isoformat()
            self.memory["metadata"]["last_updated"] = datetime.now().isoformat()
            
            # Estima contagem de tokens (aproximada)
            self._update_token_count()
            
            return True
        except Exception as e:
            print(f"Erro ao salvar plano: {e}")
            return False
    
    def add_subagent_result(self, agent_id: str, result: Dict) -> bool:
        """Adiciona resultado de um subagente"""
        try:
            result_entry = {
                "agent_id": agent_id,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            
            self.memory["subagent_results"].append(result_entry)
            self.memory["metadata"]["last_updated"] = datetime.now().isoformat()
            self._update_token_count()
            
            return True
        except Exception as e:
            print(f"Erro ao adicionar resultado do subagente: {e}")
            return False
    
    def add_sources(self, sources: List[Dict]) -> bool:
        """Adiciona fontes à memória"""
        try:
            for source in sources:
                if source not in self.memory["sources"]:
                    self.memory["sources"].append(source)
            
            self._update_token_count()
            return True
        except Exception as e:
            print(f"Erro ao adicionar fontes: {e}")
            return False
    
    def update_context(self, key: str, value: Any) -> bool:
        """Atualiza contexto específico"""
        try:
            self.memory["context"][key] = value
            self.memory["metadata"]["last_updated"] = datetime.now().isoformat()
            self._update_token_count()
            
            return True
        except Exception as e:
            print(f"Erro ao atualizar contexto: {e}")
            return False
    
    def get_research_plan(self) -> Optional[str]:
        """Recupera o plano de pesquisa"""
        return self.memory.get("research_plan")
    
    def get_query(self) -> Optional[str]:
        """Recupera a query original"""
        return self.memory.get("query")
    
    def get_subagent_results(self) -> List[Dict]:
        """Recupera todos os resultados dos subagentes"""
        return self.memory.get("subagent_results", [])
    
    def get_sources(self) -> List[Dict]:
        """Recupera todas as fontes"""
        return self.memory.get("sources", [])
    
    def get_context(self, key: str = None) -> Any:
        """Recupera contexto específico ou todo o contexto"""
        if key:
            return self.memory["context"].get(key)
        return self.memory["context"]
    
    def get_summary(self) -> Dict:
        """Recupera resumo da memória"""
        return {
            "has_plan": self.memory["research_plan"] is not None,
            "query": self.memory["query"],
            "num_subagent_results": len(self.memory["subagent_results"]),
            "num_sources": len(self.memory["sources"]),
            "token_count": self.memory["metadata"]["token_count"],
            "created_at": self.memory["metadata"]["created_at"],
            "last_updated": self.memory["metadata"]["last_updated"]
        }
    
    def is_memory_full(self) -> bool:
        """Verifica se a memória está próxima do limite"""
        return self.memory["metadata"]["token_count"] > Config.MEMORY_LIMIT_TOKENS * 0.8
    
    def clear_old_data(self) -> bool:
        """Remove dados antigos se necessário"""
        try:
            if self.is_memory_full():
                # Remove resultados mais antigos de subagentes
                if len(self.memory["subagent_results"]) > 5:
                    self.memory["subagent_results"] = self.memory["subagent_results"][-5:]
                
                # Remove fontes duplicadas ou menos relevantes
                if len(self.memory["sources"]) > 20:
                    self.memory["sources"] = self.memory["sources"][-20:]
                
                self._update_token_count()
                return True
            
            return False
        except Exception as e:
            print(f"Erro ao limpar dados antigos: {e}")
            return False
    
    def _update_token_count(self):
        """Atualiza contagem aproximada de tokens"""
        try:
            memory_str = json.dumps(self.memory, ensure_ascii=False)
            # Estimativa aproximada: 1 token ≈ 4 caracteres
            self.memory["metadata"]["token_count"] = len(memory_str) // 4
        except Exception:
            # Se der erro, define um valor padrão
            self.memory["metadata"]["token_count"] = 1000
    
    def export_memory(self) -> str:
        """Exporta memória como JSON"""
        try:
            return json.dumps(self.memory, indent=2, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao exportar memória: {e}"
    
    def import_memory(self, memory_json: str) -> bool:
        """Importa memória de JSON"""
        try:
            imported_memory = json.loads(memory_json)
            self.memory = imported_memory
            return True
        except Exception as e:
            print(f"Erro ao importar memória: {e}")
            return False

# Instância global da memória
research_memory = ResearchMemory()

@tool
def save_plan(plan: str, query: str) -> bool:
    """
    Salva o plano de pesquisa na memória.
    
    Args:
        plan: Plano de pesquisa detalhado
        query: Query original do usuário
        
    Returns:
        True se salvou com sucesso
    """
    return research_memory.save_research_plan(plan, query)

@tool
def retrieve_context() -> Dict:
    """
    Recupera todo o contexto da memória.
    
    Returns:
        Dicionário com contexto completo
    """
    return {
        "plan": research_memory.get_research_plan(),
        "query": research_memory.get_query(),
        "subagent_results": research_memory.get_subagent_results(),
        "sources": research_memory.get_sources(),
        "context": research_memory.get_context(),
        "summary": research_memory.get_summary()
    }

@tool
def add_research_result(agent_id: str, result: Dict) -> bool:
    """
    Adiciona resultado de pesquisa de um subagente.
    
    Args:
        agent_id: ID do agente que produziu o resultado
        result: Resultado da pesquisa
        
    Returns:
        True se adicionou com sucesso
    """
    return research_memory.add_subagent_result(agent_id, result)

@tool
def update_memory_context(key: str, value: str) -> bool:
    """
    Atualiza contexto específico na memória.
    
    Args:
        key: Chave do contexto
        value: Valor a ser armazenado
        
    Returns:
        True se atualizou com sucesso
    """
    return research_memory.update_context(key, value)