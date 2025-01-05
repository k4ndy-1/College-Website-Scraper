import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_top_colleges(stream, city):
  """
  Fetches top colleges from Collegesearch.in using BeautifulSoup.

  Args:
    stream: The desired academic stream (e.g., "engineering", "mbbs").
    city: The desired city (e.g., "delhi", "bangalore").

  Returns:
    A pandas DataFrame containing college names, cities, and package information.
  """
  try:
    url = f"https://www.collegesearch.in/{stream}/colleges-{city}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract college names
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

  except requests.exceptions.RequestException as
