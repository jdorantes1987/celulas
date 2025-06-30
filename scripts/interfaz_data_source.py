from abc import ABC, abstractmethod


class IDataSource(ABC):
    @abstractmethod
    def get_celulas(self):
        pass

    @abstractmethod
    def get_liderazgo(self):
        pass

    @abstractmethod
    def get_liderazgo_redes(self):
        pass

    @abstractmethod
    def get_temas(self):
        pass

    @abstractmethod
    def get_historico_celulas(self):
        pass
