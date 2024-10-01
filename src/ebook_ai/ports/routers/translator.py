from fastapi import APIRouter
from application.translator.translator import TranslatorFactory
from ports.routers.schemas.translation_schema import TranslationFileRequest, TranslationResponse, TranslationSchema
from fastapi import File, UploadFile

class TranslatorRouter():
    def __init__(self):
        self.router = APIRouter()
        self.router.post("/translate", response_model=TranslationResponse)(self.translate)
        self.router.post("/upload_file")(self.upload_file)
        self.router.post("/translate_file", response_model=TranslationResponse)(self.translate_file)

    def translate(self, translation_request: TranslationSchema) -> TranslationResponse:
        translator = TranslatorFactory.create(translation_request.client)
        translated_content = translator.translate(
            translation_request.text, translation_request.fr, translation_request.to
        )
        return TranslationResponse(
            translated_text=translated_content.content,
            token_used=translated_content.token_used,
            client=translation_request.client,
            fr=translation_request.fr,
            to=translation_request.to
        )
    
    def translate_file(self, translation_request: TranslationFileRequest) -> TranslationResponse:
        translator = TranslatorFactory.create(translation_request.client)
        translated_content = translator.translate_file(
            translation_request.file_name, translation_request.fr, translation_request.to
        )
        return TranslationResponse(
            translated_text=translated_content.content,
            token_used=translated_content.token_used,
            client=translation_request.client,
            fr=translation_request.fr,
            to=translation_request.to
        )
    
    def upload_file(self, file: UploadFile = File(...)):
        with open(f"books/{file.filename}", 'wb') as f:
            f.write(file.file.read())
        return {"filename": file.filename}