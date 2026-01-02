"""
LLaMA Service - Integration with local or cloud LLaMA models
"""
from interfaces.ai_interface import AIServiceInterface
import json
import requests
import os
from config import GEMINI_API_KEY

class LLaMAService(AIServiceInterface):
    """
    LLaMA AI Service - supports both local (Ollama) and cloud (Groq) LLaMA models
    """
    def __init__(self):
        # Try Ollama first (local), fallback to Groq (cloud)
        self.use_ollama = os.getenv("LLAMA_PROVIDER", "ollama").lower() == "ollama"
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.model = os.getenv("LLAMA_MODEL", "llama3.2")
        
        if self.use_ollama:
            print(f"LLaMA Service initialized with Ollama ({self.model})")
        else:
            print(f"LLaMA Service initialized with Groq ({self.model})")
    
    def is_available(self) -> bool:
        """Check if LLaMA service is available"""
        if self.use_ollama:
            try:
                response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
                return response.status_code == 200
            except:
                return False
        else:
            return bool(self.groq_api_key)
    
    def process_query(self, query: str, system_prompt: str):
        """Process query using LLaMA"""
        if not self.is_available():
            raise Exception("LLaMA Service not available")
        
        if self.use_ollama:
            return self._process_with_ollama(query, system_prompt)
        else:
            return self._process_with_groq(query, system_prompt)
    
    def _process_with_ollama(self, query: str, system_prompt: str):
        """Process with local Ollama"""
        try:
            url = f"{self.ollama_url}/api/generate"
            full_prompt = f"{system_prompt}\n\nUser query: {query}\n\nRespond in JSON format."
            
            response = requests.post(url, json={
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "format": "json"
            }, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "{}")
                
                # Parse JSON response
                try:
                    return json.loads(response_text)
                except:
                    # If not valid JSON, wrap in message
                    return {
                        "type": "chat",
                        "message": response_text,
                        "params": {}
                    }
            else:
                raise Exception(f"Ollama error: {response.status_code}")
                
        except Exception as e:
            print(f"Ollama Error: {e}")
            raise e
    
    def _process_with_groq(self, query: str, system_prompt: str):
        """Process with Groq Cloud"""
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                "response_format": {"type": "json_object"}
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                try:
                    return json.loads(content)
                except:
                    return {
                        "type": "chat",
                        "message": content,
                        "params": {}
                    }
            else:
                raise Exception(f"Groq error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Groq Error: {e}")
            raise e
