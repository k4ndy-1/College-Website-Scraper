import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def fetch_html(url):
    """
    Fetch the HTML content from the given URL.
    Args:
    - url (str): The target URL.
    
    Returns:
    - str: HTML content of the page.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Failed to fetch URL: {url}. Status Code: {response.status_code}")
        return None

def parse_html_table(html_content, table_id=None):
    """
    Parse HTML table dynamically based on table ID.
    Args:
    - html_content (str): The HTML content as a string.
    - table_id (str): The ID of the table to parse (optional).

    Returns:
    - DataFrame: Parsed table data as a pandas DataFrame.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Find table by ID or default to the first table
    if table_id:
        table = soup.find("table", {"id": table_id})
    else:
        table = soup.find("table")
    
    if not table:
        st.error(f"Table with ID '{table_id}' not found.")
        return pd.DataFrame()

    # Extract headers
    headers = []
    header_row = table.find("thead")
    if header_row:
        headers = [th.text.strip() for th in header_row.find_all("th")]
    
    # Extract rows
    rows = table.find("tbody").find_all("tr")
    data = []
    for row in rows:
        columns = row.find_all("td")
        row_data = [col.text.strip() for col in columns]
        data.append(row_data)

    # Handle missing headers
    if not headers and data:
        headers = [f"Column {i+1}" for i in range(len(data[0]))]

    # Ensure each row has the same number of columns as headers
    max_columns = len(headers)
    for row in data:
        while len(row) < max_columns:
            row.append(None)  # Add missing data as None
        if len(row) > max_columns:
            row = row[:max_columns]  # Truncate extra data
    
    # Create DataFrame
    return pd.DataFrame(data, columns=headers)

# URLs for College and Research rankings
urls = {
    "college": "https://www.nirfindia.org/Rankings/2024/CollegeRanking.html",
    "research": "https://www.nirfindia.org/Rankings/2024/ResearchRanking.html",
}

# Streamlit UI elements
st.title('NIRF Rankings 2024')
st.sidebar.header("Select Ranking Type")

# Get user input for ranking choice
choice = st.sidebar.radio("Choose Ranking Data", ('College', 'Research'))

st.write(f"Fetching {choice} Ranking Data...")

if choice.lower() in urls:
    url = urls[choice.lower()]
    html_content = fetch_html(url)
    
    if html_content:
        # Parse the table (specify table ID if known, else leave as None)
        table_id = "tbl_overall"  # Adjust table_id as needed or set to None
        data = parse_html_table(html_content, table_id)
        
        if not data.empty:
            # Display the data table
            st.subheader(f"{choice} Ranking Data")
            st.dataframe(data)
            
            # Option to download the data
            st.download_button(
                label="Download CSV",
                data=data.to_csv(index=False).encode('utf-8'),
                file_name=f"{choice.lower()}_ranking_2024.csv",
                mime="text/csv"
            )
        else:
            st.error(f"No data found for {choice} ranking.")
else:
    st.error("Invalid choice. Please select either 'College' or 'Research'.")
