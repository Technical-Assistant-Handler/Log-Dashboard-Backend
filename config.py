# Configuration variables

# Path to Google Cloud credentials
import json
import os
# Load Google Cloud credentials from environment variable (use the exact name from Render)
CLOUD_CREDENTIALS = "cloud_credentials.json"

# Read the JSON file and load its contents as a dictionary
try:
    with open(CLOUD_CREDENTIALS, "r") as file:
        CREDENTIALS_DICT = json.load(file)  # Correct way to parse JSON from a file
except FileNotFoundError:
    print("Error: cloud_credentials.json not found")
    CREDENTIALS_DICT = None
except json.JSONDecodeError:
    print("Error: Invalid JSON format in cloud_credentials.json")
    CREDENTIALS_DICT = None
  
IP_ADDRESS = "0.0.0.0"

# Google Sheet name
SHEET_NAME = "Technical Assistant Login Data"

# Define the scope for Google Sheets and Google Drive APIs
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Email credentials
SENDER_EMAIL = "technicalassistantshandler@gmail.com"
EMAIL_PASSWORD ="kpmk pnwe ngws xocl"


