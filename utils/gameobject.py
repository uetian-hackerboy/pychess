from abc import ABC, abstractmethod

class GameObject(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def update(self):
        pass
