from scripts.db_sqlite import BD_SQLite_Celulas as DB
from sqlite3 import connect

db_path = r"DB_Celulas.db"


class DataCelulas:
    def __init__(self) -> None:
        self.data = DB(connect(db_path))

    def celulas_activas(self):
        data = self.data.get_celulas()
        return data[data["estatus_celula"] == 1]

    def sobres_por_entregar(self):
        hist_celulas_activas = self.celulas_activas_hist()
        return hist_celulas_activas[hist_celulas_activas["sobre_entregado"] == 0]

    def celulas_activas_hist(self):
        return self.data.get_historico_celulas()

    def liderazgo(self):
        return self.data.get_liderazgo()

    def temas(self):
        return self.data.get_temas()

    def insert_hist_celulas(self, data):
        self.data.insert_hist_celulas(data)
