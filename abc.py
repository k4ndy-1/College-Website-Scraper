import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_top_colleges(course):
    """
    Fetches top colleges from Collegesearch.in based on the user's course selection.

    Args:
        course: The desired course (e.g., "engineering", "mbbs").

    Returns:
        A pandas DataFrame containing college names, cities, and package information,
        or an empty DataFrame if no data is found.
    """
    try:
        url = f"https://www.collegesearch.in/{course}"  # The URL changes based on course
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, "html.parser")

        # Fetching college names, cities, and package info (update the selectors based on actual website)
        college_names = [
            element.text.strip() 
            for element in soup.find_all("div", class_="college-name-class")  # Update with correct class or tag
        ]

        city_names = [
            element.text.strip() 
            for element in soup.find_all("span", class_="city-name-class")  # Update with correct class or tag
        ]

        package_infos = [
            element.text.strip() 
            for element in soup.find_all("span", class_="package-info-class")  # Update with correct class or tag
        ]

        # Find the minimum length of the lists to avoid errors
        min_length = min(len(college_names), len(city_names), len(package_infos))

        # Trim lists to the minimum length
        college_names = college_names[:min_length]
        city_names = city_names[:min_length]
        package_infos = package_infos[:min_length]

        # Create a DataFrame
        data = {
            "College Name": college_names,
            "City": city_names,
            "Package": package_infos,
        }
        df = pd.DataFrame(data)

        return df

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()

# Streamlit App main function
def main():
    st.title("Top Colleges Finder")

    # Ask the user to input the course they are interested in
    course = st.text_input("Enter the course (e.g., engineering, mbbs):").strip().lower()

    if st.button("Get Top Colleges"):
        if course:
            df = get_top_colleges(course)

            if not df.empty:
                st.write(f"Top Colleges for {course}:")
                st.dataframe(df)

                # Add the option to download the result as a CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"top_{course}_colleges.csv",
                    mime="text/csv"
                )
            else:
                st.write(f"No colleges found for {course}.")
        else:
            st.warning("Please enter a course name.")

if __name__ == "__main__":
    main()
