import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Function to get top colleges based on stream and city
def get_top_colleges(stream, city):
    # Setup Selenium WebDriver options for headless mode with necessary arguments
    options = Options()
    options.headless = True  # Run in headless mode (without GUI)
    options.add_argument("--no-sandbox")  # Overcome potential issue in cloud environments
    options.add_argument("--disable-dev-shm-usage")  # Fixes some issues with limited memory in cloud
    options.add_argument("--disable-gpu")  # Disable GPU to prevent issues in headless mode
    options.add_argument("--remote-debugging-port=9222")  # Set a debugging port for better stability

    # Setup WebDriver using ChromeDriverManager to automatically get the correct version
    service = Service(ChromeDriverManager().install())  # Automatically manage ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)
    
    # Modify the URL to include city and stream for search
    url = f"https://www.collegedunia.com/{stream}/{city}-colleges"
    
    try:
        # Open the page
        driver.get(url)
        
        # Wait for the page to load and the relevant element to appear
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//a[@class='jsx-3230181281 college_name underline-on-hover']/h3")
        ))

        colleges = []

        # Scrape the college names, cities, and entrance exams
        college_elements = driver.find_elements(By.XPATH, "//a[@class='jsx-3230181281 college_name underline-on-hover']/h3")
        city_elements = driver.find_elements(By.XPATH, "//span[@class='jsx-3230181281 pr-1 location']")
        package_elements = driver.find_elements(By.XPATH, "//span[contains(text(), '₹')]")  # Adjust as needed
        
        for i in range(len(college_elements)):
            college_name = college_elements[i].text.strip()
            city_name = city_elements[i].text.strip() if i < len(city_elements) else "N/A"  # Default to "N/A" if city is missing
            entrance_exam_info = package_elements[i].text.strip() if i < len(package_elements) else "N/A"  # Default to "N/A" if entrance exam info is missing

            if college_name:  # Avoid adding empty names
                colleges.append((college_name, city_name, entrance_exam_info))

        # Return the list of colleges, cities, and entrance exams
        return colleges

    except Exception as e:
        print(f"An error occurred: {e}")
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
