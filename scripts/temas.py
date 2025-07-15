from pandas import DataFrame


class Temas:
    def __init__(self, manager_sheets) -> None:
        self.oSheets = manager_sheets

    def get_temas(self) -> DataFrame:
        """
        Obtiene los datos de temas de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="temas")

    def existe_tema(self, id_tema) -> bool:
        """
        Verifica si un tema ya existe en la hoja de cálculo.
        """
        temas = self.get_temas()
        return id_tema in temas.iloc[:, 0].values

    def add_tema(self, tema_data) -> dict:
        """
        Agrega un nuevo tema a la hoja de cálculo y retorna la respuesta del API.
        """
        if self.existe_tema(tema_data[0]):
            return {"success": False, "message": "Tema ya existe."}

        response = (
            self.oSheets.get_service()
            .spreadsheets()
            .values()
            .append(
                spreadsheetId=self.oSheets.spreadsheet_id,
                range="temas",
                valueInputOption="USER_ENTERED",
                body={"values": [tema_data]},
            )
            .execute()
        )
        return {
            "success": True,
            "message": dict(updatedCells=response["updates"]["updatedCells"]),
        }
