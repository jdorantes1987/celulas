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

    def existe_registro(
        self, data_historico: DataFrame, id_celula: str, id_tema: str
    ) -> bool:
        """
        Verifica si un registro ya existe en la hoja de cálculo.
        """
        # Usa indexación booleana y .any() para verificar la existencia de forma eficiente
        existe = (
            (data_historico["id_celula"] == id_celula)
            & (data_historico["id_tema"] == id_tema)
        ).any()

        return existe

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
