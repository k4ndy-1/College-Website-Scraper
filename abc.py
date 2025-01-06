import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import re


def clean_row_data(row_text):
    """
    Cleans the row text by removing unwanted details like links, extra spaces, and hidden elements.

    Args:
        row_text: The raw text from a table row.

    Returns:
        Cleaned text.
    """
    # Remove extra spaces and unwanted content
    row_text = re.sub(r"\s{2,}", " ", row_text)  # Replace multiple spaces with a single space
    row_text = re.sub(r"\n|\t", "", row_text)  # Remove newlines and tabs
    return row_text.strip()


def scrape_nirf_rankings(category):
    """
    Scrapes NIRF India rankings for a specified category.

    Args:
        category: The category of the rankings (e.g., 'engineering', 'management', 'university').

    Returns:
        A pandas DataFrame containing the rankings data (rank, name, city, state, score).
    """
    base_url = "https://www.nirfindia.org/Rankings/2024/"
    category_url = f"{base_url}{category}Ranking.html"

    response = requests.get(category_url)
    if response.status_code != 200:
        st.error("Failed to fetch data. Please check the category.")
        return pd.DataFrame()

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "tbl_overall"})

    if not table:
        st.error("Ranking table not found.")
        return pd.DataFrame()

    # Extract all rows (both odd and even)
    rows = table.find_all("tr")[1:]  # Skip the header row

    # Initialize lists to store data
    ins_id = []
    names = []
    cities = []
    states = []
    ranks = []
    scores = []

    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 6:  # Ensure sufficient columns exist
            # Extract and clean each column's text
            inid = clean_row_data(columns[0].text.strip())
            name = clean_row_data(columns[1].text.strip())
            city = clean_row_data(columns[2].text.strip())
            state = clean_row_data(columns[3].text.strip())
            score = clean_row_data(columns[4].text.strip())
            rank = clean_row_data(columns[5].text.strip())

            # Append cleaned data to respective lists
            ins_id.append(inid)
            names.append(name)
            cities.append(city)
            states.append(state)
            scores.append(score)
            ranks.append(rank)

    # Create and return a DataFrame
    data = {
        "Institute ID": ins_id,
        "Institution Name": names,
        "City": cities,
        "State": states,
        "Rank": ranks,
        "Score": scores
    }
    return pd.DataFrame(data)


def main():
    st.title("NIRF India Rankings Scraper")

    category = st.selectbox(
        "Select the category you want to scrape:",
        ["Engineering", "Law", "Management", "University", "Medical", "Pharmacy", "Architecture"]
    )

    if st.button("Get Rankings"):
        if category:
            category_url_name = category.capitalize()  # Format the category for the URL
            df = scrape_nirf_rankings(category_url_name)

            if not df.empty:
                st.write(f"Top NIRF Rankings for {category}:")
                st.dataframe(df)

                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"nirf_{category.lower()}_rankings.csv",
                    mime="text/csv"
                )
            else:
                st.write(f"No rankings found for {category}.")
        else:
            st.warning("Please select a category.")


if __name__ == "__main__":
    main()
