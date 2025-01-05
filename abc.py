from bs4 import BeautifulSoup
import requests
import pandas as pd

def scrape_college_info(url):
  """
  Scrapes basic information (name, city, package, year estd) 
  from a given college website URL.

  Args:
    url: The URL of the college website.

  Returns:
    A dictionary containing the scraped information 
    or None if scraping fails.
  """
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes
    soup = BeautifulSoup(response.content, "html.parser")

    # Example: Basic scraping logic (adjust based on website structure)
    college_name = soup.find("h1", class_="college-name").text.strip() 
    city = soup.find("span", class_="location").text.strip() 
    try: 
      package = soup.find("p", class_="average-package").text.strip() 
    except AttributeError: 
      package = "N/A" 
    try: 
      year_estd = soup.find("span", class_="year-established").text.strip() 
    except AttributeError: 
      year_estd = "N/A" 

    return {
        "College Name": college_name,
        "City": city,
        "Package": package,
        "Year Established": year_estd
    }

  except Exception as e:
    print(f"Error scraping {url}: {e}")
    return None

# Example usage:
college_urls = [
    "https://www.collegedunia.com/", 
    "https://www.collegesearch.in/", 
]  # Replace with actual college website URLs

college_data = []
for url in college_urls:
  college_info = scrape_college_info(url)
  if college_info:
    college_data.append(college_info)

# Create a Pandas DataFrame
df = pd.DataFrame(college_data)
print(df) 

# You can further process the data (e.g., sorting, filtering)
# and display it in a user-friendly way (e.g., using Streamlit)
