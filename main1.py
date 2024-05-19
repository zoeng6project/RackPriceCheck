# get the update PC Rack Price 

from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import datetime 


url = 'https://www.petro-canada.ca/en/business/rack-prices#daily'
page = requests.get(url)
soup = BeautifulSoup(page.text,'html')
headers = soup.find_all('table')[0]. find_all ('thead')
PC_headers = [title.text  for title in headers]
PC_headers = PC_headers[0].split('\n')
PC_headers = ['PC_' + header.strip() for header in PC_headers if header.strip() != '' and header.strip() != 'Location']
df = pd.DataFrame(columns = PC_headers)
column_data = soup.find_all('tr')
for row in column_data [10:11] :
    row_data = row.find_all ('td')
    individual_row_data = [data.text.strip() for data in row_data ]
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
df = pd.DataFrame({'Name': PC_headers, 'Price': individual_row_data})
df.insert (0, 'Date', timestamp)


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

data = df.values.tolist()

result = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="PC!A:C" , 
    valueInputOption = "USER_ENTERED" , insertDataOption = "INSERT_ROWS" , body = {"values": data} ).execute()

print (result)
