from pandas import DataFrame


class Celulas:
    def __init__(self, manager_sheets) -> None:
        self.oSheets = manager_sheets

    def get_celulas(self) -> DataFrame:
        """
        Obtiene los códigos de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="celulas")

    def get_celulas_historico(self) -> DataFrame:
        """
        Obtiene el histórico de las celdas de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="hist_celulas")

    def add_actividad(self, data_actividad) -> dict:
        """
        Agrega una nueva actividad a la hoja de cálculo y retorna la respuesta del API.
        """
        response = (
            self.oSheets.get_service()
            .spreadsheets()
            .values()
            .append(
                spreadsheetId=self.oSheets.spreadsheet_id,
                range="hist_celulas",
                valueInputOption="USER_ENTERED",
                body={"values": [data_actividad]},
            )
            .execute()
        )
        return {
            "success": True,
            "message": dict(updatedCells=response["updates"]["updatedCells"]),
        }


if __name__ == "__main__":
    from scripts.data_sheets import ManageSheets

    manager_sheets = ManageSheets(
        file_sheet_name="celulas",
        spreadsheet_id="1GEtYGIQCucTTd6yVuC7dssMuJeYklbehJfWAC1UNkpE",
        credentials_file="key.json",
    )
    oData = Celulas(manager_sheets=manager_sheets)

    print(
        oData.add_actividad(
            [
                "298",
                "LD202401",
                "2025-07-07",
                "2025-07-13",
                "2025-07-13",
                "CB00055",
                "Expositor prueba",
                "TM99999999",
                "5",
                "100",
                "10",
                "1",  # Sobre entregado
                "Observación de prueba",
                "jdorantes",
                "2025-07-04 13:34:01",  # fecha de inserción
            ]
        )
    )
