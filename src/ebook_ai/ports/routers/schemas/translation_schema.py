from typing import Optional
from unittest.mock import Base
from pydantic import BaseModel

from application.translator.translator import Lang


class TranslationSchema(BaseModel):
    text: str
    client: str
    max_tokens: int
    fr: Lang
    to: Lang

class TranslationFileRequest(BaseModel):
    file_name: str
    client: str
    max_tokens: int
    fr: Lang
    to: Lang

class TranslationResponse(BaseModel):
    translated_text: Optional[str]
    token_used: Optional[int]
    client: str
    fr: Lang
    to: Lang
