def get_top_colleges(stream):
  try:
    url = f"https://www.collegesearch.in/{stream}"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")

    # Update with actual correct class names or tags
    college_names = [
        element.text.strip() 
        for element in soup.find_all("div", class_="college_text_data")  # Correct class or tag
    ]

    city_names = [
        element.text.strip() 
        for element in soup.find_all("span", class_="college_text_data")  # Correct class or tag
    ]

    package_infos = [
        element.text.strip() 
        for element in soup.find_all("span", class_="SR_college_card_bottom_data")  # Correct class or tag
    ]

    # Trim lists to minimum length
    min_length = min(len(college_names), len(city_names), len(package_infos))
    college_names = college_names[:min_length]
    city_names = city_names[:min_length]
    package_infos = package_infos[:min_length]

    data = {
        "College Name": college_names,
        "City": city_names,
        "Package": package_infos,
    }
    df = pd.DataFrame(data)

    return df

  except requests.exceptions.RequestException as e:
    st.error(f"Error fetching data: {e}")
    return pd.DataFrame()

  except Exception as e:
    st.error(f"An error occurred: {e}")
    return pd.DataFrame()
