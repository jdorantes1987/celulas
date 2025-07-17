from pandas import DataFrame


class Liderazgo:
    def __init__(self, manager_sheets) -> None:
        self.oSheets = manager_sheets

    def get_codigos(self) -> DataFrame:
        """
        Obtiene los códigos de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="codigos")

    def get_liderazgo_de_red(self) -> DataFrame:
        """
        Obtiene los datos de liderazgo de la hoja de cálculo.
        """
        return self.oSheets.get_data_hoja(sheet_name="liderazgo")

    def get_liderazgo_con_base_lider(self) -> DataFrame:
        """
        Para cada id_codigo, obtiene su cod_lider y el cod_base de ese cod_lider.
        """
        df = self.oSheets.get_data_hoja(sheet_name="liderazgo_x_codigo")
        # Realiza el self join: busca el cod_base del cod_lider
        df_join = df.merge(
            df[["id_codigo", "cod_base"]],
            left_on="cod_lider",
            right_on="id_codigo",
            how="left",
            suffixes=("", "_lider"),
        )
        # Renombra la columna cod_base_lider para mayor claridad
        df_join = df_join.rename(
            columns={
                "cod_base_lider": "cod_base_lider",
                "cod_base": "cod_base",
                "cod_base_lider": "cod_base_lider",
            }
        )
        # Selecciona las columnas relevantes
        result = df_join[
            ["id_codigo", "cod_lider", "cod_base", "cod_base_lider"]
        ].copy()
        return result

    def get_codigos_con_liderazgo(self):
        liderazgo_con_base_lider = self.get_liderazgo_con_base_lider()
        codigos = self.get_codigos()
        df_join = codigos.merge(
            liderazgo_con_base_lider,
            left_on="cod_red",
            right_on="id_codigo",
            how="left",
        )
        df_join.drop(
            columns=["id_codigo"], inplace=True
        )  # Elimina la columna id_codigo que ya no es necesaria
        # Combinancion self join para obtener cual es el lider de cada codigo
        df_join = df_join.merge(
            df_join[["id_cod", "nombre_liderazgo"]],
            left_on=["codigo_lider"],
            right_on=["id_cod"],
            how="left",
        )
        df_join.rename(
            columns={
                "id_cod_x": "id_cod",
                "id_cod": "id_cod_lider",
                "nombre_liderazgo_x": "nombre",
                "nombre_liderazgo_y": "nombre_lider",
            },
            inplace=True,
        )
        df_join["estatus"] = df_join["estatus"].fillna(1).astype(int)
        return df_join[
            [
                "id_liderazgo",
                "id_cod",
                "cod_red",
                "nombre",
                "cod_lider",
                "nombre_lider",
                "cod_base_lider",
                "estatus",
            ]
        ].copy()


if __name__ == "__main__":
    from scripts.data_sheets import ManageSheets

    manager_sheets = ManageSheets(
        file_sheet_name="celulas",
        spreadsheet_id="1GEtYGIQCucTTd6yVuC7dssMuJeYklbehJfWAC1UNkpE",
        credentials_file="key.json",
    )
    oData = Liderazgo(manager_sheets=manager_sheets)
    print(oData.get_codigos_con_liderazgo())
