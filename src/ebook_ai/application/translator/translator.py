from calendar import c
from enum import Enum
from application.ai_client import AiClient, GeminiClient, GeneratedContent, OpenAiClient
from utils.file import FileFactory
import concurrent.futures

class Lang(Enum):
    VN = "vn"
    EN = "en"

map_ai_client = {
    "gemini": GeminiClient,
    "openai": OpenAiClient
}

class Translator:
    def __init__(self, ai_client: AiClient) -> None:
        self.ai_client = ai_client

    def translate(self, text: str, fr: Lang, to: Lang) -> GeneratedContent:
        instruction = f"You are a professional translator. Please translate the provided content from {fr.value} to {to.value}"
        generated_content = self.ai_client.generate(text, instruction)
        return generated_content
    
    def translate_file(self, file_name: str, fr: Lang, to: Lang) -> GeneratedContent:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        file_process = FileFactory.create(file_name)
        book, items = file_process.read(f"books/{file_name}")
        token_used = 0
        for item in items:
            data_future = []
            soup, p_tags = file_process.get_p_tags(item)
            for p in p_tags:
                if p.string and len(p.string) > 30:
                    data_future.append(executor.submit(self.process_p, p, fr, to))
            concurrent.futures.wait(data_future)
            for token in data_future:
                token_used += token.result()
            item.content = str(soup)
        file_process.write(f"books/translations/{file_name}", book)
        self.ai_client.close()
        return GeneratedContent(content="Translation completed", token_used=None)
    
    def process_p(self, p, fr: Lang, to: Lang) -> int:
        generated_content = self.translate(p.string, fr, to)
        p.string = generated_content.content
        return generated_content.token_used or 0

class TranslatorFactory:
    @staticmethod
    def create(ai_client: str) -> Translator:
        return Translator(map_ai_client[ai_client]())