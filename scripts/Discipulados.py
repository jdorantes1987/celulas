from pandas import DataFrame


class Discipulados:
    def __init__(self, manager_sheets) -> None:
        self.oSheets = manager_sheets

    def get_discipulados(self) -> DataFrame:
        """
        Obtiene los códigos de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="discipulados")

    def get_discipulados_historico(self) -> DataFrame:
        """
        Obtiene los discipulados historicos de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="hist_discipulados")

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
                range="hist_discipulados",
                valueInputOption="USER_ENTERED",
                body={"values": [data_actividad]},
            )
            .execute()
        )
        return {
            "success": True,
            "message": dict(updatedCells=response["updates"]["updatedCells"]),
        }
