import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime

def format_elapsed_time(start_time: float) -> str:
    """Formata tempo decorrido de forma legível"""
    elapsed = time.time() - start_time
    
    if elapsed < 60:
        return f"{elapsed:.1f} segundos"
    elif elapsed < 3600:
        minutes = elapsed / 60
        return f"{minutes:.1f} minutos"
    else:
        hours = elapsed / 3600
        return f"{hours:.1f} horas"

def print_research_status(step: str, details: str = ""):
    """Imprime status da pesquisa de forma consistente"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {step}")
    if details:
        print(f"          {details}")

def truncate_text(text: str, max_length: int = 200) -> str:
    """Trunca texto mantendo palavras completas"""
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.8:  # Se encontrou espaço em posição razoável
        return truncated[:last_space] + "..."
    else:
        return truncated + "..."

def extract_domain_from_url(url: str) -> str:
    """Extrai domínio de uma URL"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return url

def clean_text(text: str) -> str:
    """Limpa texto removendo caracteres especiais desnecessários"""
    import re
    
    # Remove múltiplos espaços
    text = re.sub(r'\s+', ' ', text)
    
    # Remove quebras de linha excessivas
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    
    # Remove caracteres de controle
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
    
    return text.strip()

def count_tokens_approximate(text: str) -> int:
    """Conta tokens de forma aproximada (1 token ≈ 4 caracteres)"""
    return len(text) // 4

def format_company_list(companies: List[Dict]) -> str:
    """Formata lista de empresas de forma legível"""
    if not companies:
        return "Nenhuma empresa encontrada."
    
    formatted = "## Empresas Encontradas\n\n"
    
    for i, company in enumerate(companies, 1):
        formatted += f"### {i}. {company.get('name', 'Nome não disponível')}\n"
        
        if 'website' in company:
            formatted += f"**Website:** {company['website']}\n"
        
        if 'description' in company:
            description = truncate_text(company['description'], 150)
            formatted += f"**Descrição:** {description}\n"
        
        if 'industry' in company:
            formatted += f"**Indústria:** {company['industry']}\n"
        
        if 'location' in company:
            formatted += f"**Localização:** {company['location']}\n"
        
        formatted += "\n"
    
    return formatted

def validate_search_results(results: List[Dict]) -> List[Dict]:
    """Valida e limpa resultados de pesquisa"""
    valid_results = []
    
    for result in results:
        if not isinstance(result, dict):
            continue
        
        # Verifica campos obrigatórios
        if not result.get('title') and not result.get('content'):
            continue
        
        # Limpa e valida campos
        cleaned_result = {
            'title': clean_text(result.get('title', 'Sem título')),
            'url': result.get('url', ''),
            'content': clean_text(result.get('content', '')),
            'score': float(result.get('score', 0.5))
        }
        
        # Adiciona metadados
        cleaned_result['domain'] = extract_domain_from_url(cleaned_result['url'])
        cleaned_result['content_length'] = len(cleaned_result['content'])
        cleaned_result['validated_at'] = datetime.now().isoformat()
        
        valid_results.append(cleaned_result)
    
    return valid_results

def merge_duplicate_sources(sources: List[Dict]) -> List[Dict]:
    """Remove fontes duplicadas mantendo a melhor qualidade"""
    seen_urls = {}
    merged_sources = []
    
    for source in sources:
        url = source.get('url', '')
        
        if not url:
            merged_sources.append(source)
            continue
        
        if url in seen_urls:
            # Mantém a fonte com melhor score
            existing_idx = seen_urls[url]
            existing_score = merged_sources[existing_idx].get('score', 0)
            current_score = source.get('score', 0)
            
            if current_score > existing_score:
                merged_sources[existing_idx] = source
        else:
            seen_urls[url] = len(merged_sources)
            merged_sources.append(source)
    
    return merged_sources

def generate_research_summary(results: Dict[str, Any]) -> str:
    """Gera resumo executivo da pesquisa"""
    if not results.get('success'):
        return f"❌ Pesquisa falhou: {results.get('error', 'Erro desconhecido')}"
    
    metadata = results.get('metadata', {})
    query = results.get('query', 'Query não especificada')
    
    summary = f"""
## Resumo da Pesquisa

**Query:** {query}

**Resultados:**
- ✅ Pesquisa concluída com sucesso
- 🤖 {metadata.get('num_subagents', 0)} subagentes executados
- 📚 {metadata.get('num_sources', 0)} fontes consultadas
- 🔄 {metadata.get('iterations', 0)} iterações realizadas

**Status:** Completo
    """.strip()
    
    return summary

def save_research_to_file(results: Dict[str, Any], filename: Optional[str] = None) -> str:
    """Salva resultados da pesquisa em arquivo"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        query_safe = "".join(c for c in results.get('query', 'research')[:50] if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"research_{query_safe}_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Relatório de Pesquisa Multi-Agente\n\n")
            f.write(f"**Gerado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n\n")
            f.write(generate_research_summary(results))
            f.write("\n\n")
            f.write("---\n\n")
            f.write(results.get('final_report', 'Relatório não disponível'))
        
        return filename
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return ""

def print_progress_bar(current: int, total: int, width: int = 50):
    """Imprime barra de progresso"""
    if total == 0:
        return
    
    progress = current / total
    filled = int(width * progress)
    bar = "█" * filled + "░" * (width - filled)
    percentage = progress * 100
    
    print(f"\r[{bar}] {percentage:.1f}% ({current}/{total})", end="", flush=True)
    
    if current >= total:
        print()  # Nova linha quando completo

class ResearchTimer:
    """Classe para cronometrar etapas da pesquisa"""
    
    def __init__(self):
        self.start_time = time.time()
        self.steps = {}
    
    def mark_step(self, step_name: str):
        """Marca timestamp de uma etapa"""
        current_time = time.time()
        self.steps[step_name] = {
            'timestamp': current_time,
            'elapsed_from_start': current_time - self.start_time
        }
    
    def get_step_duration(self, step_name: str, previous_step: str = None) -> float:
        """Calcula duração de uma etapa"""
        if step_name not in self.steps:
            return 0.0
        
        if previous_step and previous_step in self.steps:
            return self.steps[step_name]['timestamp'] - self.steps[previous_step]['timestamp']
        else:
            return self.steps[step_name]['elapsed_from_start']
    
    def get_total_elapsed(self) -> float:
        """Retorna tempo total decorrido"""
        return time.time() - self.start_time
    
    def print_timing_report(self):
        """Imprime relatório de timing"""
        print("\n⏱️  Relatório de Timing:")
        print("-" * 40)
        
        previous_step = None
        for step_name, step_data in self.steps.items():
            duration = self.get_step_duration(step_name, previous_step)
            print(f"{step_name}: {format_elapsed_time(time.time() - duration)}")
            previous_step = step_name
        
        print("-" * 40)
        print(f"Total: {format_elapsed_time(self.get_total_elapsed())}")

def create_progress_callback():
    """Cria callback de progresso para usar com agentes"""
    progress_state = {'current': 0, 'total': 0}
    
    def update_progress(current: int = None, total: int = None, message: str = ""):
        if total is not None:
            progress_state['total'] = total
        if current is not None:
            progress_state['current'] = current
        
        if message:
            print(f"\n{message}")
        
        if progress_state['total'] > 0:
            print_progress_bar(progress_state['current'], progress_state['total'])
    
    return update_progress