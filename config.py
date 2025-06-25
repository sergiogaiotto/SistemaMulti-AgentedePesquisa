import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    """Configurações do sistema"""
    
    # APIs
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    # Modelo
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
    
    # Pesquisa
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
    MAX_SUBAGENTS = int(os.getenv("MAX_SUBAGENTS", "3"))
    MEMORY_LIMIT_TOKENS = int(os.getenv("MEMORY_LIMIT_TOKENS", "200000"))
    
    @classmethod
    def validate(cls):
        """Valida se as configurações obrigatórias estão definidas"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY é obrigatório. Configure no arquivo .env")
        
        print("✅ Configurações validadas com sucesso!")
        return True