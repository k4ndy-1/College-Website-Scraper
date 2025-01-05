import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

# Function to get top colleges based on stream and city
def get_top_colleges(stream, city):
    url = f"https://www.collegedunia.com/{stream}/{city}-colleges"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    colleges = []
    
    try:
        # Use BeautifulSoup to extract data
        college_elements = soup.select("a.jsx-3230181281.college_name.underline-on-hover h3")
        city_elements = soup.select("span.jsx-3230181281.pr-1.location")
        package_elements = soup.select("span:contains('₹')")
        
        for i in range(len(college_elements)):
            college_name = college_elements[i].get_text(strip=True)
            city_name = city_elements[i].get_text(strip=True) if i < len(city_elements) else "N/A"
            entrance_exam_info = package_elements[i].get_text(strip=True) if i < len(package_elements) else "N/A"
            
            if college_name:
                colleges.append((college_name, city_name, entrance_exam_info))

        return colleges

    except Exception as e:
        print(f"Error occurred: {e}")
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
