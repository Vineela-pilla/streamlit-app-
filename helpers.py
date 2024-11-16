import openai
import pandas as pd
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
import gspread 
from oauth2client.service_account import ServiceAccountCredentials 
from googleapiclient.discovery import build
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

def load_csv_data(file_path):
    """Load CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def load_google_sheet(sheet_name, worksheet_name="sheet1"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\VINEELA\\Downloads\\credentials.json.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).worksheet(worksheet_name)
    
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    
    return df

def search_with_serpapi(query):
    """Search using SerpAPI."""
    search = GoogleSearch({"q": query, "api_key": SERP_API_KEY})
    results = search.get_dict().get("organic_results", [])
    return results

def query_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:  
        print(f"An error occurred: {e}")


