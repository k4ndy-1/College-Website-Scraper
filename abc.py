import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st
import pandas as pd

# Function to get top colleges based on stream and city
def get_top_colleges(stream, city):
    options = Options()
    options.headless = True  # Running in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')  # Disable GPU usage in headless mode
    options.add_argument('--remote-debugging-port=9222')  # This option is often needed to avoid errors in headless mode
    
    # Setup ChromeDriver with options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://www.collegedunia.com/{stream}/{city}-colleges"  # Modify URL if necessary
    driver.get(url)

    # Wait for the page to load and ensure dynamic content has been rendered
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='jsx-3230181281 college_name underline-on-hover']/h3"))
        )

        colleges = []
        
        # Scrape the college names, city, and entrance exam details
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
        print(f"Error occurred while scraping: {e}")
        return []

    finally:
        driver.quit()  # Always close the WebDriver

# Streamlit App main function
def main():
    st.title("Top Colleges Finder")

    stream = st.text_input("Enter the s
