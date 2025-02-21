# Configuration variables

# Path to Google Cloud credentials
import os
CREDENTIALS_PATH = os.path.abspath("C:/Users/Fadhi Safeer/OneDrive/Documents/Internship/Technical Assistant Dashboard/dashboard/backend/cloud_credentials.json")
IP_ADDRESS = "127.0.0.1"

# Google Sheet name
SHEET_NAME = "Technical Assistant Login Data"

# Define the scope for Google Sheets and Google Drive APIs
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Email credentials
SENDER_EMAIL = "technicalassistantshandler@gmail.com"
