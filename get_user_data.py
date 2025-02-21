import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import config

def get_user_log_data():
    # Use credentials to create a client to interact with the Google Drive API
    scope = config.SCOPE
    creds = ServiceAccountCredentials.from_json_keyfile_dict(config.CREDENTIALS_DICT, config.SCOPE)

    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open(config.SHEET_NAME)

    # Open Sheet2
    sheet1 = sheet.get_worksheet(1)
    today_date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    data = sheet1.get_all_records()

    matched_users = []

    for row in data:
        date_cell = row.get('Date')
        tp_cell = row.get('TP Number')
        username = row.get('Username')
        login_time = row.get('Login Time')
        logout_time_cell = row.get('Logout Time')
        time_diff = row.get('Time Difference')

        if (str(date_cell).strip() == str(today_date).strip() and
            (logout_time_cell is None or str(logout_time_cell).strip() == "")):

            matched_users.append({
                "tpnumber": tp_cell,
                "username": username,
                "login_time": login_time
            })

    return matched_users if matched_users else [{"message": "User not found or already logged out", "status": False}]

def verify_tpnumber(tpnumber):
    # Use credentials to create a client to interact with the Google Drive API
    scope = config.SCOPE
    creds = ServiceAccountCredentials.from_json_keyfile_name(config.CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open(config.SHEET_NAME)

    # Open Sheet1
    sheet1 = sheet.get_worksheet(0)
    data = sheet1.get_all_records()

    tpnumber_present = False

    for row_index, row in enumerate(data, start=2):  # start=2 to account for header row
        tp_cell = sheet1.cell(row_index, 1).value  # First column in the row
        if str(tp_cell).strip() == str(tpnumber).strip():
            tpnumber_present = True
            break

    return tpnumber_present
