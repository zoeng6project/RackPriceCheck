import pandas as pd 
import requests
import pdfplumber
import pandas as pd 
import time
from datetime import datetime 

# Download the PDF file
url = 'https://valeroapps.valero.com/public/rpt_Terminal_Rack_Prices.pdf'
response = requests.get(url)
pdf_path = 'rpt_Terminal_Rack_Prices.pdf' 
with open(pdf_path, 'wb') as file:
    file.write(response.content)


# Open the downloaded PDF file with pdfplumber
with pdfplumber.open(pdf_path) as pdf:
    # Extract tables from each page
    for page in pdf.pages:
        tables = page.extract_tables()
        
        # Check if tables were found on the page
        if len(tables) > 0:
            # Extract the first table from the list of tables
            first_table = tables[0]
            print(first_table)
            break  # Stop iterating through the pages after finding the first table


column = first_table[0:1]
df = pd.DataFrame(first_table[2:3], columns = column)
df2 = df.T
df3 = df2[2:21]

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

df3.insert (0, 'Date', timestamp)
df3.reset_index(inplace=True)


# Access google drive
from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'key.json'
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1kRMf2mfHSKf1KzCFwxTG7z3K_7LEomJStB4Tr78LV0s"
service = build("sheets", "v4", credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

# insert rows 

data = df3.values.tolist()

result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Canada_E10!A:C" , 
    valueInputOption = "USER_ENTERED" , insertDataOption = "INSERT_ROWS" , body = {"values": data} ).execute()

print (result)


