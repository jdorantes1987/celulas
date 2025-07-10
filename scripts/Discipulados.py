class Discipulados:
    def __init__(self, manager_sheets) -> None:
        self.oSheets = manager_sheets

    def get_discipulados(self):
        """
        Obtiene los códigos de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="discipulados")


if __name__ == "__main__":
    from scripts.data_sheets import ManagerSheets

    manager_sheets = ManagerSheets(
        file_sheet_name="celulas",
        spreadsheet_id="1GEtYGIQCucTTd6yVuC7dssMuJeYklbehJfWAC1UNkpE",
        credentials_file="key.json",
    )
    oData = Discipulados(manager_sheets=manager_sheets)
    print(oData.get_discipulados())
