import time
import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# Function to get top colleges based on stream and city
def get_top_colleges(stream, city):
    # Path to the locally uploaded chromedriver (ensure it's in the right folder)
    chromedriver_path = "./drivers/chromedriver"  # Ensure the correct path to chromedriver

    # Setting up Selenium with headless Chrome
    options = Options()
    options.headless = True  # Run in headless mode (no GUI)
    options.add_argument("--no-sandbox")  # Overcome potential issue in cloud environments
    options.add_argument("--disable-dev-shm-usage")  # Fixes some issues with limited memory in cloud

    # Set the ChromeDriver Service
    service = Service(chromedriver_path)  # Use the path to your local ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)

    # URL of the colleges page based on stream and city
    url = f"https://www.collegedunia.com/{stream}/{city}-colleges"  # You may need to adjust this URL format

    try:
        # Open the page
        driver.get(url)
        
        # Wait for the page content to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='jsx-3230181281 college_name underline-on-hover']/h3"))
        )

        colleges = []
        
        # Scrape college name, city, and entrance exam details
        college_elements = driver.find_elements(By.XPATH, "//a[@class='jsx-3230181281 college_name underline-on-hover']/h3")
        city_elements = driver.find_elements(By.XPATH, "//span[@class='jsx-3230181281 pr-1 location']")
        package_elements = driver.find_elements(By.XPATH, "//span[contains(text(), '₹')]")

        # Extract data and store in the list
        for i in range(len(college_elements)):
            college_name = college_elements[i].text.strip()
            city_name = city_elements[i].text.strip() if i < len(city_elements) else "N/A"
            entrance_exam_info = package_elements[i].text.strip() if i < len(package_elements) else "N/A"
            
            if college_name:  # Avoid adding empty names
                colleges.append((college_name, city_name, entrance_exam_info))

        return colleges

    except Exception as e:
        print(f"Error occurred while scraping: {e}")
        return []

    finally:
        # Quit the driver to clean up resources
        driver.quit()


# Streamlit App main function
def main():
    # Set up the Streamlit interface
    st.title("Top Colleges Finder")

    # Ask the user for the stream and city they are interested in
    stream = st.text_input("Enter the stream (e.g., MBBS, Engineering, Law):").strip().lower()
    city = st.text_input("Enter the city (e.g., Delhi, Bangalore, Mumbai):").strip().lower()

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
