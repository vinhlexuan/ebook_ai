from dataclasses import dataclass
from typing import Optional, Protocol
from openai import OpenAI
import os

@dataclass
class GeneratedContent:
    content: Optional[str]
    token_used: Optional[int]

class AiClient(Protocol):
    def generate(self, text: str, instruction: Optional[str] = None) -> GeneratedContent:
        ...

    def close(self):
        ...

class GeminiClient(AiClient):
    def __init__(self) -> None:
        self.client = None

    def generate(self, text: str, instruction: Optional[str] = None):
        return "Gemini generated text"

    def close(self):
        pass
    
class OpenAiClient(AiClient):
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key= os.getenv("OPENAI_API_KEY")
        )
    def generate(self, text: str, instruction: Optional[str] = None) -> GeneratedContent:
        model = "gpt-3.5-turbo"
        messages = []
        if instruction:
            messages.append({"role": "system", "content": instruction})
        messages.append({"role": "user", "content": text})
        response = self.client.chat.completions.create(
            model=model, 
            messages=messages
        )
        return GeneratedContent(
            content=response.choices[0].message.content,
            token_used=response.usage.total_tokens if response.usage else None
        )
    def close(self):
        self.client.close()