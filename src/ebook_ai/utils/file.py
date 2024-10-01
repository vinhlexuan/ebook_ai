from ast import List
from hmac import new
from typing import Callable, Optional, Protocol, Tuple
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

class FileType(Protocol):
    def read(self, file_path: str):
        ...
    
    def write(self, file_path: str, book):
        ...

    def get_p_tags(self, item) -> Tuple[BeautifulSoup, list]:
        ...

class FileFactory:
    @staticmethod
    def create(file_name: str) -> FileType:
        if file_name.endswith('.epub'):
            return EpubFile()
        elif file_name.endswith('.pdf'):
            return PdfFile()
        else:
            raise ValueError('Unsupported file type')
        
class PdfFile(FileType):
    def __init__(self) -> None:
        pass

    def read(self, file_path: str) -> list:
        ...

    def write(self, file_path: str, book):
        ...

    def get_p_tags(self, item) ->  Tuple[BeautifulSoup, list]:
        ...
    
class EpubFile(FileType):
    def __init__(self) -> None:
        pass

    def read(self, file_path: str):
        book = epub.read_epub(file_path)
        items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        return book, items

    def write(self, file_path: str, book):
        epub.write_epub(file_path, book)
    
    def get_p_tags(self, item) -> Tuple[BeautifulSoup, list]:
        soup = BeautifulSoup(item.get_body_content(), 'html.parser')
        return soup, soup.find_all('p')
