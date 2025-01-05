from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # Import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import streamlit as st
from bs4 import BeautifulSoup

# ------------- Settings for Pages -----------
st.set_page_config(layout="wide")

# Function to get website content (general scraper)
def get_website_content(url):
    driver = None
    content = None  # Store the content here
    
    try:
        # Setup headless mode for Chrome
        options = Options()  # Use the imported Options class
        options.add_argument('--headless')  # Run Chrome in headless mode
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1200')

        # Initialize the Chrome WebDriver with the Service and Options correctly
        service = Service(ChromeDriverManager().install())  # Initialize Service correctly
        driver = webdriver.Chrome(service=service, options=options)

        st.write(f"DEBUG:DRIVER:{driver}")
        
        # Get the webpage content
        driver.get(url)
        time.sleep(5)
        
        # Get the page source HTML
        html_doc = driver.page_source
        content = BeautifulSoup(html_doc, 'html.parser')  # Parse with BeautifulSoup

        driver.quit()

    except Exception as e:
        st.write(f"DEBUG:INIT_DRIVER:ERROR:{e}")
    finally:
        if driver is not None:
            driver.quit()
    
    return content  # Return the BeautifulSoup object

# Function to get top colleges based on stream and city
def get_top_colleges(stream, city):
    driver = None
    colleges = []

    try:
        # Setup Service for WebDriver
        service = Service(ChromeDriverManager().install())  # Initialize Service correctly
        options = Options()  # Use the imported Options class
        options.headless = True  # Headless mode (no GUI)

        # Launch Chrome with the specified Service and Options
        driver = webdriver.Chrome(service=service, options=options)

        # Modify the URL to include city (we're assuming a city filter can be added in the URL)
        url = f"https://www.collegedunia.com/{stream}/{city}-colleges"  # Update the URL format if needed
        
        # Open the page
        driver.get(url)

        # Wait for the page to load (use explicit wait)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='jsx-3230181281 college_name underline-on-hover']/h3")))

        # Scrape the college names, cities, entrance exams, and cutoff
        college_elements = driver.find_elements(By.XPATH, "//a[@class='jsx-3230181281 college_name underline-on-hover']/h3")
        city_elements = driver.find_elements(By.XPATH, "//span[@class='jsx-3230181281 pr-1 location']")
        package_elements = driver.find_elements(By.XPATH, "//span[contains(text(), '₹')]")  # Entrance exams info (adjust XPath if needed)

        for i in range(len(college_elements)):
            college_name = college_elements[i].text.strip()
            city_name = city_elements[i].text.strip() if i < len(city_elements) else "N/A"  # Default to "N/A" if city is missing
            entrance_exam_info = package_elements[i].text.strip() if i < len(package_elements) else "N/A"  # Default to "N/A" if entrance exam info is missing

            if college_name:  # Avoid adding empty names
                colleges.append((college_name, city_name, entrance_exam_info))

        return colleges

    except Exception as e:
        st.write(f"An error occurred while scraping colleges: {e}")
        return []

    finally:
        if driver is not None:
            driver.quit()

# Example usage in your Streamlit app
if __name__ == "__main__":
    # Stream and city filter inputs (for example, you can take them from the user)
    stream = "engineering"  # Replace with dynamic input
    city = "delhi"  # Replace with dynamic input

    # Scraping website content
    website_url = "https://www.collegedunia.com"  # Replace with the URL you want to scrape
    website_content = get_website_content(website_url)
    
    # Display website content on the Streamlit app
    st.write(website_content)

    # Get top colleges based on stream and city
    colleges = get_top_colleges(stream, city)
    
    # Display college information on Streamlit
    st.write(f"Top Colleges for {stream} in {city}:")
    for college in colleges:
        st.write(f"College: {college[0]}, City: {college[1]}, Entrance Exam: {college[2]}")
