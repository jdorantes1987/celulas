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
