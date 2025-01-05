import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import pandas as pd

# ------------- Settings for Pages -----------
st.set_page_config(layout="wide")

# Function to get website content
def get_website_content(url):
    driver = None
    try:
        # Setup the driver
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920x1200')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # Wait until the page is fully loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        html_doc = driver.page_source
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup.get_text()

    except Exception as e:
        st.write(f"ERROR: {e}")
    finally:
        if driver:
            driver.quit()
    return None

# Extract college details from the website
def site_extraction_page(stream,city):
    SAMPLE_URL = "https://www.collegedunia.com"
    url = st.text_input(label="URL", placeholder="https://example.com", value=SAMPLE_URL)

    clicked = st.button("Load Page Content",type="primary")
    if clicked:
        colleges = []
        
        try:
            # Scrape college data using Selenium
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)

            # Wait for the page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Use the XPath to find the required elements
            college_elements = driver.find_elements(By.XPATH, "//a[@class='jsx-3230181281 college_name underline-on-hover']/h3")
            city_elements = driver.find_elements(By.XPATH, "//span[@class='jsx-3230181281 pr-1 location']")
            package_elements = driver.find_elements(By.XPATH, "//span[contains(text(), '₹')]")

            # Process the data
            for i in range(len(college_elements)):
                college_name = college_elements[i].text.strip()
                city_name = city_elements[i].text.strip() if i < len(city_elements) else "N/A"
                entrance_exam_info = package_elements[i].text.strip() if i < len(package_elements) else "N/A"
                
                if college_name:  # Avoid empty names
                    colleges.append((college_name, city_name, entrance_exam_info))

            driver.quit()
            return colleges
        except Exception as e:
            st.write(f"An error occurred: {e}")
            return []
        finally:
            if driver:
                driver.quit()

# Streamlit App main function
def main():
    # Set up the Streamlit interface
    st.title("Top Colleges Finder")

    # Ask the user for the stream and city they are interested in
    stream = st.text_input("Enter the stream (e.g., MBBS, Engineering, Law):").strip().lower()
    city = st.text_input("Enter the city (e.g., Delhi, Bangalore, Mumbai):").strip().lower()

    # Check if the user has provided input
    if st.button("Get Top Colleges"):
        if stream and city:
            # Get the top colleges for the stream and city
            colleges = site_extraction_page(stream, city)

            if colleges:
                # Convert the list of tuples into a DataFrame
                df = pd.DataFrame(colleges, columns=["College Name", "City", "Package"])

                # Display the results in a table
                st.write(f"Top Colleges for {stream} in {city}:")
                st.dataframe(df)

                # Provide download option
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"top_{stream}_{city}_colleges.csv",
                    mime="text/csv"
                )

            else:
                st.write(f"No colleges found for {stream} in {city}. Please try again later.")
        else:
            st.warning("Please enter both stream and city.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
