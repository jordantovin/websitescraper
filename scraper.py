import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

URL = "https://www.booooooom.com/"  # CHANGE THIS
SPREADSHEET_NAME = "Scraped Data"  # CHANGE THIS
WORKSHEET_NAME = "Sheet1"

def scrape():
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for a in soup.find_all("a"):
        name = a.get_text(strip=True)
        link = a.get("href")

        if name and link:
            results.append([name, link])

    return results


def upload_to_sheets(rows):
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=scopes
    )

    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)
    sheet.append_rows(rows)


if __name__ == "__main__":
    rows = scrape()
    if rows:
        upload_to_sheets(rows)
        print(f"Uploaded {len(rows)} rows")
    else:
        print("No data found")
