import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import re

def clean_text(row_text):
    """
    Cleans unwanted patterns from the text, such as 'More DetailsClose', 'TLR (100)', 'RPC (100)', etc.
    
    Args:
        row_text: The raw text from a table row.
        
    Returns:
        Cleaned text.
    """
    # Remove unwanted patterns using regular expressions
    unwanted_patterns = [
        r"More Details.*",  # Matches 'More Details' and everything after
        r"TLR \(.*?\)",     # Matches 'TLR (100)' and similar patterns
        r"RPC \(.*?\)",     # Matches 'RPC (100)' and similar patterns
        r"GO \(.*?\)",      # Matches 'GO (100)' and similar patterns
        r"OI \(.*?\)",      # Matches 'OI (100)' and similar patterns
        r"PERCEPTION \(.*?\)",  # Matches 'PERCEPTION (100)' and similar patterns
        r"\|",              # Matches the pipe character '|'
        r"\s{2,}",          # Matches multiple spaces and replaces them with a single space
        r"\d+\.\d{2}",      # Matches any decimal number like '80.01', '95.79', etc.
    ]
    
    for pattern in unwanted_patterns:
        row_text = re.sub(pattern, "", row_text)

    return row_text.strip()

def scrape_nirf_rankings(category):
    """
    Scrapes NIRF India rankings for a specified category.

    Args:
        category: The category of the rankings (e.g., 'engineering', 'management', 'university').

    Returns:
        A pandas DataFrame containing the rankings data (rank, name, city, score).
    """

    # Base URL and the category URL pattern
    base_url = "https://www.nirfindia.org/Rankings/2024/" 
    category_url = f"{base_url}{category}Ranking.html" 

    response = requests.get(category_url)

    if response.status_code != 200:
        st.error("Failed to fetch data. Please check the category.")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, "html.parser")

    # Find the ranking table using the provided table ID
    table = soup.find("table", {"id": "tbl_overall"})

    if not table:
        st.error("Ranking table not found")
        return pd.DataFrame()

    # Parse the table rows
    rows = table.find_all("tr")[1:]  # Skip header row
    
    # Extracting the required details
    ins_id = []
    ranks = []
    names = []
    cities = []
    scores = []
    states = []

    for row in rows:
        columns = row.find_all("td")
        if len(columns) > 1:
            # Extract raw data from the columns and clean it
            inid = clean_text(columns[0].text.strip())
            name = clean_text(columns[1].text.strip())
            city = clean_text(columns[2].text.strip())
            state = clean_text(columns[3].text.strip())
            rank = clean_text(columns[4].text.strip())
            score = clean_text(columns[-1].text.strip())  # Assuming the last column contains the score

            # Check if city and state are not empty after cleaning
            if not city or not state:
                continue  # Skip the row if city or state is missing

            # Append cleaned data to lists
            ins_id.append(inid)
            names.append(name)
            cities.append(city)
            states.append(state)
            ranks.append(rank)
            scores.append(score)

    # Create a DataFrame
    data = {
        "Institute ID": ins_id,
        "Institution Name": names,
        "City": cities,
        "State": states,
        "Rank": ranks,
        "Score": scores,
    }

    df = pd.DataFrame(data)
    return df


# Streamlit App main function
def main():
    st.title("NIRF India Rankings Scraper")

    # Ask the user to input the category
    category = st.selectbox(
        "Select the category you want to scrape:",
        ["Engineering", "Law", "Management", "University", "Medical", "Pharmacy", "Architecture"],
    )

    if st.button("Get Rankings"):
        if category:
            # Convert category to the appropriate format for the URL
            category_url_name = category.capitalize()
            df = scrape_nirf_rankings(category_url_name)

            if not df.empty:
                st.write(f"Top NIRF Rankings for {category.capitalize()}:")

                # Show all rows without skipping
                st.dataframe(df)

                # Add the option to download the result as a CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"nirf_{category.lower()}_rankings.csv",
                    mime="text/csv",
                )
            else:
                st.write(f"No rankings found for {category.capitalize()}.")
        else:
            st.warning("Please select a category.")

if __name__ == "__main__":
    main()
