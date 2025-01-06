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

    # Find all rows regardless of odd/even
    rows = table.find_all("tr", {"role": "row"})[1:]  # Skip header row

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
            # Extract and clean data
            inid = clean_row_data(columns[0].text.strip())
            name = clean_row_data(columns[1].text.strip())
            
            # Remove unwanted embedded elements
            name = re.sub(r"<.*?>", "", columns[1].text.strip(), flags=re.DOTALL)

            city = clean_row_data(columns[2].text.strip())
            state = clean_row_data(columns[3].text.strip())
            score = clean_row_data(columns[4].text.strip())
            rank = clean_row_data(columns[5].text.strip())

            # Append cleaned data to lists
            ins_id.append(inid)
            names.append(name)
            cities.append(city)
            states.append(state)
            ranks.append(rank)
            scores.append(score)

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
