from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
from helpers import load_csv_data, load_google_sheet, search_with_serpapi, query_openai

st.title("AI Agent: Search & Retrieve Information")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
sheet1= st.text_input("Enter Google Sheet name (if using Sheets):")
if uploaded_file is not None:
    df = load_csv_data(uploaded_file)
    st.write("CSV Data Loaded:")
    st.dataframe(df)
elif sheet1:
    df = load_google_sheet(sheet1)
    st.write(f"Google Sheet Data Loaded ({sheet1}):")
    st.dataframe(df)
search_query = st.text_input("Enter search query")
if search_query and df is not None:
    column_name = st.selectbox("Choose a column for search:", df.columns)
    search_results = []
    for entity in df[column_name]:
        search_results_entity = search_with_serpapi(f"{search_query} for {entity}")
        st.write(f"Search results for {entity}:")
        st.json(search_results_entity)
        formatted_result = query_openai(f"Summarize the following search results:\n{search_results_entity}")
        search_results.append({
            "Entity": entity,
            "Search Results": search_results_entity,
            "Formatted Result": formatted_result
        })

    result_df = pd.DataFrame(search_results)
    st.write("Formatted Results:")
    st.dataframe(result_df)

    csv = result_df.to_csv(index=False)
    st.download_button("Download Search Results", csv, "search_results.csv", "text/csv")

