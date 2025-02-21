import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

import pytz
import config
import datetime

kl_timezone = pytz.timezone("Asia/Kuala_Lumpur")

def user_authentication(tpnumber, password):
    # Use credentials to create a client to interact with the Google Drive API
    scope = config.SCOPE
    creds = ServiceAccountCredentials.from_json_keyfile_dict(config.CREDENTIALS_DICT, config.SCOPE)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open(config.SHEET_NAME)

    # Open Sheet1
    sheet1 = sheet.get_worksheet(0)
    data = sheet1.get_all_records()

    # Check if tpnumber and password are present
    for row in data:
        if str(row['TP Number']).strip() == str(tpnumber).strip() and str(row['Password']).strip() == str(password).strip():
            username = str(row['Username']).strip()
            login_date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
            login_time = datetime.datetime.now(kl_timezone).strftime("%I:%M %p")

            # Append to Sheet2
            sheet2 = sheet.get_worksheet(1)
            sheet2.append_row([login_date, tpnumber, username, login_time])

            return {"message": "Login successful", "username": username}

    return {"message": "Authentication failed"}


def append_logout_time(tpnumber):
    # Use credentials to create a client to interact with the Google Drive API
    scope = config.SCOPE
    creds = ServiceAccountCredentials.from_json_keyfile_dict(config.CREDENTIALS_DICT, config.SCOPE)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open(config.SHEET_NAME)

    # Open Sheet1
    sheet1 = sheet.get_worksheet(1)
    today_date = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    data = sheet1.get_all_records()

    logout_successful = False

    for row_index, row in enumerate(data, start=2):  # start=2 to account for header row
        
        date_cell = row.get('Date')
        tp_cell = row.get('TP Number')
        logout_time_cell = row.get('Logout Time')



        
        if (str(date_cell).strip() == str(today_date).strip() and
            str(tp_cell).strip() == str(tpnumber) and
            (logout_time_cell is None or str(logout_time_cell).strip() == "")):


            logout_time = datetime.datetime.now(kl_timezone).strftime("%I:%M %p")
            #print(logout_time)
            sheet1.update_cell(row_index, 5, logout_time)  # Assuming Logout Time is in 5th column

            login_time_cell = row.get('Login Time')
            try:
                if login_time_cell is None or str(login_time_cell).strip() == "":
                    logging.error(f"Missing login time for TP Number {tpnumber}. Skipping.")
                    continue  # Skip processing this row if login time is missing

                logging.info(f"Login Time: {login_time_cell}")

                # Convert to 24-hour format automatically
                login_time = datetime.datetime.strptime(login_time_cell.strip(), "%I:%M %p")
                logout_time_obj = datetime.datetime.strptime(logout_time.strip(), "%I:%M %p")

                # Calculate time difference
                time_diff = logout_time_obj - login_time
                logging.info(f"Time difference: {time_diff}")

                sheet1.update_cell(row_index, 6, str(time_diff))  # Assuming Time Difference is in 6th column
                
                logout_successful = True

            except Exception as e:
                logging.error(f"Error processing row for TP Number {tpnumber}: {e}")

    return {"message": "Logout successful"} if logout_successful else {"message": "Logout failed"}

