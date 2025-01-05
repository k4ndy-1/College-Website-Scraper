import streamlit as st
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

# ------------- Settings for Pages -----------
st.set_page_config(layout="wide")

# Keep text only
def get_website_content(url):
    driver = None
   
    try:
        # Using on Local
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1200')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)
        st.write(f"DEBUG:DRIVER:{driver}")
        driver.get(url)
        time.sleep(5)
        html_doc = driver.page_source
        
        driver.quit()
        
    except Exception as e:
        st.write(f"DEBUG:INIT_DRIVER:ERROR:{e}")
    finally:
        if driver is not None: driver.quit()
    return None


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
