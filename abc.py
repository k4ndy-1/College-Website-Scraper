import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller  # Automatic driver installer
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# ------------- Settings for Pages -----------
st.set_page_config(layout="wide")

# Function to get website content
def get_website_content(url):
    driver = None
    content = None
    
    try:
        # Automatically install and set up ChromeDr # This will download and install the correct ChromeDriver version automatically
        
        # Set Chrome options (headless)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1200')
        
        # Setup the WebDriver
        driver = webdriver.Chrome(options=options)

        # Fetch the webpage
        driver.get(url)
        time.sleep(5)  # Ensure the page loads
        
        # Get the page HTML and parse it with BeautifulSoup
        html_doc = driver.page_source
        content = BeautifulSoup(html_doc, 'html.parser')
        
    except Exception as e:
        st.write(f"DEBUG: ERROR: {e}")
    finally:
        if driver is not None:
            driver.quit()

    return content

# Function to scrape top colleges based on stream and city
def get_top_colleges(stream, city):
    driver = None
    colleges = []

    try:
        # Automatically install and set up ChromeDrive
        # Set Chrome options (headless)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1200')

        # Setup the WebDriver
        driver = webdriver.Chrome(options=options)

        # Modify the URL to include city and stream
        url = f"https://www.collegedunia.com/{stream}/{city}-colleges"
        driver.get(url)

        # Wait for the page to load completely
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='jsx-3230181281 college_name underline-on-hover']/h3")))

        # Scrape college names, cities, entrance exams, and cutoffs
        college_elements = driver.find_elements(By.XPATH, "//a[@class='jsx-3230181281 college_name underline-on-hover']/h3")
        city_elements = driver.find_elements(By.XPATH, "//span[@class='jsx-3230181281 pr-1 location']")
        package_elements = driver.find_elements(By.XPATH, "//span[contains(text(), '₹')]")

        for i in range(len(college_elements)):
            college_name = college_elements[i].text.strip()
            city_name = city_elements[i].text.strip() if i < len(city_elements) else "N/A"
            entrance_exam_info = package_elements[i].text.strip() if i < len(package_elements) else "N/A"

            if college_name:
                colleges.append((college_name, city_name, entrance_exam_info))

        return colleges

    except Exception as e:
        st.write(f"An error occurred: {e}")
        return []

    finally:
        if driver is not None:
            driver.quit()

# Example usage in Streamlit
if __name__ == "__main__":
    # Get user input for stream and city (or set default values for testing)
    stream = "engineering"  # You can modify this to get dynamic input from Streamlit UI
    city = "delhi"  # Modify this similarly to get dynamic input

    # Scrape top colleges
    colleges = get_top_colleges(stream, city)

    # Display the scraped college data in Streamlit
    st.write(f"Top Colleges for {stream} in {city}:")
    for college in colleges:
        st.write(f"College: {college[0]}, City: {college[1]}, Entrance Exam: {college[2]}")
