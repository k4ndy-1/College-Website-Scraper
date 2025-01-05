import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_top_colleges(stream):
  """
  Fetches top colleges from Collegesearch.in using BeautifulSoup.

  Args:
    stream: The desired academic stream (e.g., "engineering", "mbbs").

  Returns:
    A pandas DataFrame containing college names, cities, and package information,
    or an empty DataFrame if no data is found.
  """
  try:
    url = f"https://www.collegesearch.in/{stream}"  # Adjust URL as needed
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract college names (adjust XPath as needed)
    college_names = [
        element.text.strip() 
        for element in soup.find_all("a", class_="jsx-3230181281 college_name underline-on-hover")
    ]

    # Extract city names (adjust XPath as needed)
    city_names = [
        element.text.strip() 
        for element in soup.find_all("span", class_="jsx-3230181281 pr-1 location") 
    ]

    # Extract package information (adjust XPath as needed)
    package_infos = [
        element.text.strip() 
        for element in soup.find_all("span", text=True) 
        if "₹" in element.text
    ]

    # Find the minimum length of the lists to avoid errors
    min_length = min(len(college_names), len(city_names), len(package_infos))

    # Trim lists to the minimum length
    college_names = college_names[:min_length]
    city_names = city_names[:min_length]
    package_infos = package_infos[:min_length]

    # Create a DataFrame
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

# Streamlit App main function
def main():
  st.title("Top Colleges Finder")

  stream = st.text_input("Enter the stream (e.g., engineering, mbbs):").strip().lower()

  if st.button("Get Top Colleges"):
    if stream:
      df = get_top_colleges(stream)

      if not df.empty:
        st.write(f"Top Colleges for {stream}:")
        st.dataframe(df)

        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"top_{stream}_colleges.csv",
            mime="text/csv"
        )
      else:
        st.write(f"No colleges found for {stream}.")
    else:
      st.warning("Please enter the stream.")

if __name__ == "__main__":
  main()
