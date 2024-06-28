from scripts.db_sqlite import BD_SQLite_Celulas as DB
from sqlite3 import connect

db_path = r'DB_Celulas.db'
    
class DataDiscipulados:        
    def __init__(self) -> None:
        self.data = DB(connect(db_path))
    
    def liderazgo(self):
        return self.data.get_liderazgo()
    
    def liderazgo_redes(self):
        return self.data.get_liderazgo_redes()
    
    def insert_hist_discipulados(self, data):
        self.data.insert_hist_discipulados(data)