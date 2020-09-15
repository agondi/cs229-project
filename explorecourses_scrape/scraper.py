import requests
import csv
from bs4 import BeautifulSoup

URL = "https://explorecourses.stanford.edu/print?filter-catalognumber-CS=on&filter-catalognumber-CS=on&q=CS&descriptions=on&schedules=on"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='printSearchResults')
course_elems = results.find_all("div", class_="searchResult")

filename = "courses.csv" 
f = open(filename, "w") 

#write header rows
headers = "Course Number, Course Title, Units, Instructor(s), Terms, Last Offered, Ways, Course Description\n" 
f.write(headers)

for course_elem in course_elems:
    
    waysExist = False
    currOffer = False
    instructorNamed = False
    courseNumber = course_elem.find('span', class_='courseNumber')
    remColon = courseNumber.text.find(":")
    courseNumber = courseNumber.text[:remColon]
    courseTitle = course_elem.find('span', class_='courseTitle')
    courseDescription = course_elem.find('div', class_='courseDescription')
    courseAttribute = course_elem.find_all('div', class_='courseAttributes')
    courseAttributes = courseAttribute[0]
    if len(courseAttribute) > 1:
        instructorNamed = True
        instructor = courseAttribute[1]
    if "Last offered" in courseAttributes.text:
        currOffer = True
        lastOffered = courseAttributes.text.split("|")[0].split("Last offered: ")[1]
    if len(courseAttributes.text.split("|")[0].split("Terms: ")) > 1:
        courseTerms = courseAttributes.text.split("|")[0].split("Terms: ")[1]
    courseUnits = courseAttributes.text.split("|")[1].split("Units:")[1]
    if len(courseAttributes.text.split("|")) > 2:
        if "UG Reqs" in courseAttributes.text.split("|")[2]:
            waysExist = True
            courseWays = courseAttributes.text.split("|")[2].split("UG Reqs:")[1].replace(",", "|")
            res = courseWays.find('WAY-')
            courseWays = courseWays[res:]
    f.write(courseNumber.strip() + "," + courseTitle.text.strip().replace(",", "|") + "," + courseUnits.strip() + ", ")
    if instructorNamed == True: 
        f.write(instructor.text.strip().split("Instructors: ; ")[1].replace(",", " ") + ", ")
    else:
        f.write(" " + ", ")
    if currOffer == False: 
        f.write(courseTerms.strip().replace(",", "|") + ", ")
    else:
        f.write(" " + ", ")
    if currOffer == True: 
        f.write(lastOffered.strip() + ", ")
    else:
        f.write(" " + ", ")
    if waysExist == True: 
        f.write(courseWays.strip()+ ", ")
    else:
        f.write(" " + ", ")
    f.write(courseDescription.text.strip().replace(",", " ") +  "\n")
