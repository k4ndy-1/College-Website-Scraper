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
    
    # URL based on the selected category
    category_url = f"{base_url}{category}Ranking.html"
    response = requests.get(category_url)
    
    if response.status_code != 200:
        st.error("Failed to fetch data. Please check the category.")
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the ranking table (this needs to be customized based on the actual structure of the table)
    table = soup.find("table", {"class": "table table-bordered"})

    if not table:
        st.error("Ranking table not found")
        return pd.DataFrame()

    # Parse the table rows
    rows = table.find_all("tr")[1:]  # Skip header row
    
    # Extracting the required details
    ranks = []
    names = []
    cities = []
    scores = []
    
    for row in rows:
        columns = row.find_all("td")
        if len(columns) > 1:
            rank = columns[0].text.strip()
            name = columns[1].text.strip()
            city = columns[2].text.strip()
            score = columns[-1].text.strip()  # Assuming the last column contains the score
            
            ranks.append(rank)
            names.append(name)
            cities.append(city)
            scores.append(score)

    # Create a DataFrame
    data = {
        "Rank": ranks,
        "Institution Name": names,
        "City": cities,
        "Score": scores
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
