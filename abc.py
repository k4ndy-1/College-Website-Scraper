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

    # Parse the table rows, skipping odd rows
    rows = table.find_all("tr")[1::2]  # Skip header row and all odd rows

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
            # Extract raw data from the columns
            inid = columns[0].text.strip()
            name = columns[1].text.strip()
            city = columns[2].text.strip()
            state = columns[3].text.strip()
            rank = columns[4].text.strip()
            score = columns[-1].text.strip()  # Assuming the last column contains the score

            # Append raw data to lists
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

                # Skip odd rows before displaying
                df_even_rows = df[df.index % 2 == 0] 
                st.dataframe(df_even_rows) 

                # Add the option to download the result as a CSV
                csv = df_even_rows.to_csv(index=False)  # Use df_even_rows for CSV download
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
