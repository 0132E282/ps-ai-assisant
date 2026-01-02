from abc import ABC, abstractmethod

class STTServiceInterface(ABC):
    @abstractmethod
    def transcribe(self, audio_file_path: str) -> str:
        pass

    @abstractmethod
    def listen_and_transcribe(self) -> str:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass
