from scripts.db_sqlite import BD_SQLite_Celulas as DB
from sqlite3 import connect

db_path = r'DB_Celulas.db'
    
class DataCelulas:        
    def __init__(self) -> None:
        self.data = DB(connect(db_path))
    
    def celulas_activas(self):
        return self.data.get_celulas_activas()
        
    def liderazgo(self):
        return self.data.get_liderazgo()
    
    def temas(self):
        return self.data.get_temas()
    
    def insert_hist_celulas(self, data):
        self.data.insert_hist_celulas(data)