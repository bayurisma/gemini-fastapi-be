from abc import ABC, abstractmethod
from pathlib import Path

class FileProcessor(ABC):
    @abstractmethod
    def supports(self, mime_type: str) -> bool:
        pass
    
    @abstractmethod
    def process(self, path: Path, filename: str, mime_type: str):
        pass