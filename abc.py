import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def scrape_nirf_rankings(category):
    """
    Scrapes NIRF India rankings for a specified category.

    Args:
        category: The category of the rankings (e.g., 'engineering', 'management', 'university').

    Returns:
        A pandas DataFrame containing the rankings data (Institute ID, Name, City, State, Score, Rank).
    """
    # Base URL and the category URL pattern
    base_url = "https://www.nirfindia.org/Rankings/2024/"
    
    # URL based on the selected category
    category_url = f"{base_url}{category}Ranking.html"
    response = requests.get(category_url)
    
    if response.status_code != 200:
        st.error(f"Failed to fetch data from {category_url}. Please check the category.")
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the ranking table using the provided table ID
    table = soup.find("table", {"id": "tbl_overall"})

    if not table:
        st.error("Ranking table not found. Please check the category URL.")
        return pd.DataFrame()

    # Parse the table rows, skipping the header row
    rows = table.find_all("tr")[1:]

    # Extracting the required details
    institute_ids = []
    names = []
    cities = []
    states = []
    scores = []
    ranks = []
    
    for row in rows:
        columns = row.find_all("td")
        
        # Ensure that the row has enough columns to extract the data
        if len(columns) >= 6:  # We expect at least 6 columns (Institute ID, Name, City, State, Score, Rank)
            try:
                # Extracting each column based on the expected structure
                institute_id = columns[0].text.strip()   # Institute ID
                name = columns[1].text.strip()            # Name
                city = columns[2].text.strip()            # City
                state = columns[3].text.strip()           # State
                score = columns[4].text.strip()           # Score
                rank = columns[5].text.strip()            # Rank

                # Append to lists
                institute_ids.append(institute_id)
                names.append(name)
                cities.append(city)
                states.append(state)
                scores.append(score)
                ranks.append(rank)
            except IndexError:
                st.warning("Error processing a row in the table. Skipping this row.")
                continue  # Skip the current row if an IndexError occurs
        else:
            st.warning("Skipping malformed row with insufficient columns.")
            continue  # Skip rows that don't have the expected number of columns

    # Create a DataFrame
    data = {
        "Institute ID": institute_ids,
        "Name": names,
        "City": cities,
        "State": states,
        "Score": scores,
        "Rank": ranks
    }
    
    df = pd.DataFrame(data)
    return df

# Streamlit App main function
def main():
    st.title("NIRF India Rankings Scraper")

    # Ask the user to input the category
    category = st.selectbox(
        "Select the category you want to scrape:",
        ["Engineering", "Law", "Management", "University", "Medical", "Pharmacy", "Architecture"]
    )

    # Scrape the data for the selected category
    if st.button("Get Rankings"):
        if category:
            # Convert category to the appropriate format for the URL
            category_url_name = category.capitalize()  # Ensuring the first letter is capitalized
            df = scrape_nirf_rankings(category_url_name)

            if not df.empty:
                st.write(f"Top NIRF Rankings for {category.capitalize()}:")
                st.dataframe(df)

                # Add the option to download the result as a CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"nirf_{category.lower()}_rankings.csv",
                    mime="text/csv"
                )
            else:
                st.write(f"No rankings found for {category.capitalize()}.")
        else:
            st.warning("Please select a category.")

if __name__ == "__main__":
    main()
