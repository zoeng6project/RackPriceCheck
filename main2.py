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
            
            
            
# exract table into dataframe
column = first_table[0:1]
df = pd.DataFrame(first_table[1:30], columns = column)
df2 = df.iloc[:,[0 , 4]]

now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

df2.insert (0, 'Date', timestamp)

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

data = df2.values.tolist()

result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Valero!A:C" , 
    valueInputOption = "USER_ENTERED" , insertDataOption = "INSERT_ROWS" , body = {"values": data} ).execute()

print (result)
