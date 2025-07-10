class Discipulados:
    def __init__(self, manager_sheets) -> None:
        self.oSheets = manager_sheets

    def get_discipulados(self):
        """
        Obtiene los códigos de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="discipulados")
