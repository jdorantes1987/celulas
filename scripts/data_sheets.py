from pandas import DataFrame
import gspread

from oauth2client.service_account import ServiceAccountCredentials


class ManagerSheets:
    def __init__(self, file_sheet_name, spreadsheet_id, credentials_file):
        self.file_sheet_name = file_sheet_name
        self.spreadsheet_id = spreadsheet_id
        self.credentials_file = credentials_file
        self.spreadsheet = self._get_spreadsheet()

    def _get_spreadsheet(self):
        # Autenticación y acceso a Google Sheets
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        # Cambia aquí: usa from_json_keyfile_dict si credentials_file es un dict
        if isinstance(self.credentials_file, dict):
            self.creds = ServiceAccountCredentials.from_json_keyfile_dict(
                self.credentials_file, self.scope
            )
        else:
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_file, self.scope
            )
        client = gspread.authorize(self.creds)
        return client.open(self.file_sheet_name)

    def get_data_hoja(self, sheet_name=None) -> DataFrame:
        # Selecciona la hoja de Google Sheets
        worksheet = self.spreadsheet.worksheet(sheet_name)
        # Obtiene todos los valores de la hoja de cálculo
        data = DataFrame(
            worksheet.get_all_values()[1:],  # ignora la primera fila de encabezados
            columns=worksheet.get_all_values()[
                0
            ],  # obtiene la primera fila como encabezados
        )
        return data


if __name__ == "__main__":
    import toml

    # Carga las variables de entorno desde un archivo .toml
    config = toml.load(r".streamlit\\config.toml")
    SPREADSHEET_ID = config.get("google_sheets", {}).get("CELULAS_ID")
    FILE_CELULAS_NAME = config.get("google_sheets", {}).get("FILE_CELULAS_NAME")
    SHEET_NAME = config.get("google_sheets", {}).get("SHEET_TEMAS")
    # Obtener la sección como diccionario
    CREDENTIALS_FILE = dict(config["google_service_account"])

    oTemas = ManagerSheets(
        file_sheet_name=FILE_CELULAS_NAME,
        spreadsheet_id=SPREADSHEET_ID,
        credentials_file=CREDENTIALS_FILE,
    )
    print(oTemas.get_data_hoja(sheet_name=SHEET_NAME))
