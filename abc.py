import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Function to get top colleges based on stream and city
def get_top_colleges(stream, city):
    # Setup Selenium WebDriver to use Browserless.io service
    options = Options()
    options.headless = True  # Set to True to run headless
    
    # Use Browserless.io endpoint URL and set up the proxy (your own browserless.io URL or any other service)
    options.add_argument('--remote-debugging-port=9222')  # You can pass the Browserless URL here
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    # Create a Service instance for Browserless
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = f"https://www.collegedunia.com/{stream}/{city}-colleges"  # Example URL format, update as needed
    driver.get(url)

    # Wait for the page to load and elements to become available
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class='jsx-3230181281 college_name underline-on-hover']/h3")))

    colleges = []

    try:
        # Scrape the college names, cities, entrance exams, and cutoff using XPaths
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
        print(f"Error occurred: {e}")
        return []

    finally:
        # Close the WebDriver session
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
            colleges = get_top_colleges(stream, city)

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
