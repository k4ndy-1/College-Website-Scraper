import time
import streamlit as st
import pandas as pd
from seleniumbase import BaseCase

# Function to get top colleges based on stream and city
def get_top_colleges(stream, city):
    # Launch the browser using SeleniumBase
    with BaseCase() as self:
        self.open(f"https://www.collegedunia.com/{stream}/{city}-colleges")
        
        # Wait for page content to load
        self.wait_for_element("//a[@class='jsx-3230181281 college_name underline-on-hover']/h3")

        colleges = []
        try:
            # Scrape the college names, city, and entrance exam details
            college_elements = self.find_elements("//a[@class='jsx-3230181281 college_name underline-on-hover']/h3")
            city_elements = self.find_elements("//span[@class='jsx-3230181281 pr-1 location']")
            package_elements = self.find_elements("//span[contains(text(), '₹')]")
            
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

# Streamlit App main function
def main():
    st.title("Top Colleges Finder")

    stream = st.text_input("Enter the stream (e.g., MBBS, Engineering, Law):").strip().lower()
    city = st.text_input("Enter the city (e.g., Delhi, Bangalore, Mumbai):").strip().lower()

    if st.button("Get Top Colleges"):
        if stream and city:
            colleges = get_top_colleges(stream, city)

            if colleges:
                df = pd.DataFrame(colleges, columns=["College Name", "City", "Package"])
                st.write(f"Top Colleges for {stream} in {city}:")
                st.dataframe(df)

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

if __name__ == "__main__":
    main()
