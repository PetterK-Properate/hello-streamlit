import gspread
from google.oauth2.service_account import Credentials

def get_google_sheets_data(source_sheet_id, source_sheet_name, target_sheet_id, target_sheet_name, tfm_sys=360):
    # Authenticate and open the source sheet
    creds = Credentials.from_service_account_file('service_account.json', scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)
    
    source_sheet = client.open_by_key(source_sheet_id).worksheet(source_sheet_name)
    target_sheet = client.open_by_key(target_sheet_id).worksheet(target_sheet_name)
    
    source_data = source_sheet.get_all_values()
    target_data = target_sheet.get_all_values()
    
    specific_values = ['Bacnet_device']
    
    for i, row in enumerate(source_data[2:], start=3):
        value_aa = row[26]  # Column AA
        if value_aa == str(tfm_sys):
            value_j = row[9]  # Column J
            if value_j == '' or value_j in specific_values:
                combined_value = ''.join(row[28:35])  # Columns AC to AI
                for target_row in target_data[1:]:
                    if target_row[10] == combined_value:  # Column K
                        source_sheet.update_cell(i, 5, target_row[0])  # Column E
                        break

    return source_data
