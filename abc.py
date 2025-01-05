import requests
from bs4 import BeautifulSoup

def get_top_colleges(stream, city):
    url = f"https://www.collegedunia.com/{stream}/{city}-colleges"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    colleges = []
    
    try:
        # Use BeautifulSoup to parse the data from the HTML
        college_elements = soup.select("a.jsx-3230181281.college_name.underline-on-hover h3")
        city_elements = soup.select("span.jsx-3230181281.pr-1.location")
        package_elements = soup.select("span:contains('₹')")  # Adjust if needed
        
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

