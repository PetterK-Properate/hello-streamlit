import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

def process_files(source_sheet_id, source_sheet_name, target_sheet_id, target_sheet_name, specific_values, tfm_sys):
    # Authenticate and connect to the Google Sheets API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file('path/to/your/service_account.json', scopes=scope)
    client = gspread.authorize(creds)

    try:
        # Open the source sheet
        source_sheet = client.open_by_key(source_sheet_id).worksheet(source_sheet_name)
        source_data = source_sheet.get_all_values()[2:]  # Skip the first two rows

        # Open the target sheet
        target_sheet = client.open_by_key(target_sheet_id).worksheet(target_sheet_name)
        target_data = target_sheet.get_all_values()

        # Process each row in the source sheet
        for i, row in enumerate(source_data):
            value_aa = row[26]  # Column AA is index 26 (0-indexed)

            if value_aa == str(tfm_sys):
                value_j = row[9]  # Column J is index 9

                if value_j == '' or value_j in specific_values:
                    combined_values = ''.join(row[28:35])  # Columns AC to AI are indices 28 to 34

                    # Check if the combined value exists in column K of the target sheet
                    match_found = False
                    for target_row in target_data[1:]:
                        if target_row[10] == combined_values:  # Column K is index 10
                            value_to_copy = target_row[0]  # Column A is index 0
                            source_sheet.update_cell(i + 3, 5, value_to_copy)  # Column E is index 4
                            match_found = True
                            break

                    if not match_found:
                        print(f'No match found in target sheet for combined string: {combined_values}')

    except Exception as e:
        print(f'Error: {e}')

# Example usage
source_sheet_id = '1tgaca6MmB3YIKXblBu6c_jIWrBAeWwmarv7LAcCCylU'
source_sheet_name = 'NB2_edit'
target_sheet_id = '1u_YYF_SafcDt8AzuK_mQdAU7vek49txPPlmxC9E_1zo'
target_sheet_name = 'Description'
specific_values = ['Bacnet_device']
tfm_sys = 360

process_files(source_sheet_id, source_sheet_name, target_sheet_id, target_sheet_name, specific_values, tfm_sys)
