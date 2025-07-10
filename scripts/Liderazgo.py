class Liderazgo:
    def __init__(self, manager_sheets) -> None:
        self.oSheets = manager_sheets

    def get_codigos(self):
        """
        Obtiene los códigos de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="codigos")

    def get_liderazgo(self):
        """
        Obtiene los datos de liderazgo de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="liderazgo")

    def get_liderazgo_x_codigo(self):
        """
        Obtiene los datos de liderazgo por código de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="liderazgo_x_codigo")


if __name__ == "__main__":
    from scripts.data_sheets import ManagerSheets

    manager_sheets = ManagerSheets(
        file_sheet_name="celulas",
        spreadsheet_id="1GEtYGIQCucTTd6yVuC7dssMuJeYklbehJfWAC1UNkpE",
        credentials_file="key.json",
    )
    oData = Liderazgo(manager_sheets=manager_sheets)
    print(oData.get_codigos())
