# agents/__init__.py
"""Módulo de agentes do sistema multi-agente de pesquisa"""

from .lead_researcher import lead_researcher, create_research_plan, synthesize_research_results
from .search_subagent import run_subagent, create_subagent
from .citation_agent import citation_agent, process_documents_for_citations

__all__ = [
    'lead_researcher',
    'create_research_plan', 
    'synthesize_research_results',
    'run_subagent',
    'create_subagent',
    'citation_agent',
    'process_documents_for_citations'
]

# tools/__init__.py
"""Ferramentas do sistema de pesquisa"""

from .web_search import search_web, search_companies, web_search_tool
from .citation_tools import add_citations_to_report, extract_key_facts, format_company_info

__all__ = [
    'search_web',
    'search_companies', 
    'web_search_tool',
    'add_citations_to_report',
    'extract_key_facts',
    'format_company_info'
]

# memory/__init__.py
"""Sistema de memória para pesquisa multi-agente"""

from .research_memory import (
    research_memory, 
    save_plan, 
    retrieve_context, 
    add_research_result,
    update_memory_context
)

__all__ = [
    'research_memory',
    'save_plan',
    'retrieve_context', 
    'add_research_result',
    'update_memory_context'
]

# utils/__init__.py
"""Utilitários do sistema"""

from .helpers import (
    format_elapsed_time,
    print_research_status,
    truncate_text,
    clean_text,
    format_company_list,
    generate_research_summary,
    save_research_to_file,
    ResearchTimer
)

__all__ = [
    'format_elapsed_time',
    'print_research_status', 
    'truncate_text',
    'clean_text',
    'format_company_list',
    'generate_research_summary',
    'save_research_to_file',
    'ResearchTimer'
]

# graph/__init__.py
"""Workflow de pesquisa usando LangGraph"""

from .research_workflow import research_workflow, MultiAgentResearchWorkflow, ResearchState

__all__ = [
    'research_workflow',
    'MultiAgentResearchWorkflow', 
    'ResearchState'
]