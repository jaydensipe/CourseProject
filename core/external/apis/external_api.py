from abc import ABC, abstractmethod


class ExternalAPI(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def process_input(self):
        pass

    @abstractmethod
    def set_token(self):
        pass
