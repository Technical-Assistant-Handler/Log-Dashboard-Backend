# Configuration variables

# Path to Google Cloud credentials
import os
# Load Google Cloud credentials from environment variable (use the exact name from Render)
CLOUD_CREDENTIALS = os.getenv("CLOUD_CREDENTIALS")

# Convert JSON string to dictionary
if CLOUD_CREDENTIALS:
    CREDENTIALS_DICT = json.loads(CLOUD_CREDENTIALS)  # Use this in your code
else:
    CREDENTIALS_DICT = None  # Handle missing credentials
  
IP_ADDRESS = "0.0.0.0"

# Google Sheet name
SHEET_NAME = "Technical Assistant Login Data"

# Define the scope for Google Sheets and Google Drive APIs
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Email credentials
SENDER_EMAIL = "technicalassistantshandler@gmail.com"


