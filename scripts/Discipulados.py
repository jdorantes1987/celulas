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

    def existe_registro(
        self, data_historico: DataFrame, id_discipulado: str, fecha: str
    ) -> bool:
        """
        Verifica si un registro ya existe en la hoja de cálculo.
        """
        # Asegúrate de que la columna 'fecha' sea del tipo datetime
        data_historico["fecha"] = data_historico["fecha"].astype("datetime64[ns]")
        # Usa indexación booleana y .any() para verificar la existencia de forma eficiente
        existe = (
            (data_historico["id_discipulado"] == id_discipulado)
            & (data_historico["fecha"].dt.strftime("%Y-%m-%d") == fecha)
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


if __name__ == "__main__":
    from scripts.data_sheets import ManageSheets

    manager_sheets = ManageSheets(
        file_sheet_name="celulas",
        spreadsheet_id="1GEtYGIQCucTTd6yVuC7dssMuJeYklbehJfWAC1UNkpE",
        credentials_file="key.json",
    )
    oData = Discipulados(manager_sheets=manager_sheets)
    print(
        oData.existe_registro(
            oData.get_discipulados_historico(), "DCP23_7", "2025-07-20"
        )
    )
