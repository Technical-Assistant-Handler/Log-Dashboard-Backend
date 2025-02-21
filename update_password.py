import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import logging
import config

            
def update_password(tpnumber, new_password):
    # Use credentials to create a client to interact with the Google Drive API
    scope = config.SCOPE
    creds = ServiceAccountCredentials.from_json_keyfile_name(config.CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open(config.SHEET_NAME)

    # Open Sheet1
    sheet1 = sheet.get_worksheet(0)
    data = sheet1.get_all_records()

    password_updated = False

    for row_index, row in enumerate(data, start=2):  # Start at 2 to account for header row
        tp_cell = sheet1.cell(row_index, 1).value  # First column in the row
        if str(tp_cell).strip() == str(tpnumber).strip():
            sheet1.update_cell(row_index, 3, new_password)  # Third column in the row
            password_updated = True
            break

    return {"message": "Password updated successfully"} if password_updated else {"message": "TP number not found"}

