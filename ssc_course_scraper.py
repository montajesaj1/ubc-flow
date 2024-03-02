from bs4 import BeautifulSoup as bs
import requests
import regex as re
from pprint import pprint


def get_soup(dept: str = None, number: str = None, section: str = None) -> bs:
    if not dept and not number and not section:
        webpage = requests.get(
            r"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-all-departments"
        )
    elif dept and not number and not section:
        webpage = requests.get(
            rf"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-department&dept={dept}"
        )
    elif dept and number and not section:
        webpage = requests.get(
            rf"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept={dept}&course={number}"
        )
    elif dept and number and section:
        webpage = requests.get(
            rf"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept={dept}&course={number}&section={section}"
        )
    else:
        raise Exception("Combination to get soup not correct!")

    if webpage.status_code != 200:
        raise Exception("The webpage is not reachable code: {webpage.status_code}")

    return bs(webpage.text, "html.parser")


def get_course_instructors(dept: str, number: int, section: int) -> list:
    """
    Given a UBC course code, number, and section return table of information
    """

    soup = get_soup(dept, number, section)
    instructor_table = (soup.findAll("table", attrs={"class", "table"}))[2]
    return [x.get_text(strip=True) for x in instructor_table.findAll("a")]


def get_course_sections(dept: str, number: int) -> dict:
    """
    Given a UBC course code & number, returns a dict of some fields
    """

    soup = get_soup(dept, number)
    content_expand = soup.find("div", attrs={"class", "content expand"})

    credits = content_expand.find(string=re.compile(rf"^Credits: ")).split()[1]

    # not sure if works on course page because of the index might not be the same needs testing
    # pre_req_str = content_expand.findAll('p')[2]
    # Alberto: found a solution to pull Pre-reqs data. if nothing is found, pre_req_str will be an empty string.
    pre_req_str = ""
    elements = soup.find_all("p")
    for e in elements:
        if "Pre-reqs:" in e.get_text():
            pre_req_str = e.get_text()
    # pre_req_str needs joining and sanitization/separation using the old code I(Shorya) wrote

    # Alberto: next few lines is for pulling course description
    # assuming every ssc course page will have a h4 element contianing the course page
    # find the h4 element and check if the next element is a p element 
    course_description = ''
    h4_element = soup.find('h4')
    h4_next_sibling = h4_element.find_next_sibling()
    if h4_next_sibling.name == 'p':
        # Access p element, hopefully the p element is the description
        course_description = h4_next_sibling.text  

    # narrowing to the section we need - the whole table and then only keeping the Lecture sections
    section_table = content_expand.find(
        "table", attrs={"class": "table table-striped section-summary"}
    )
    lecture_rows = section_table.find_all("tr", attrs={"class": "section1"})

    # dividing the section row into specific fields
    sections = []
    day_time = {}
    for row in lecture_rows:
        td_tags = row.findAll("td")
        section = td_tags[1].find("a", href=True)
        if not section:
            section = sections[len(sections) - 1]
        else:
            section = section.get_text(strip=True)[-3:]
        if section.isdigit():
            if section not in sections:
                sections.append(section)
            days = td_tags[6].get_text(strip=True).split(" ")
            start_time = td_tags[7].get_text(strip=True)
            end_time = td_tags[8].get_text(strip=True)
            if section not in day_time:
                day_time[section] = {}
            for day in days:
                day_time[section].update({day: (start_time, end_time)})

    return {
        "description": course_description,
        "credits": credits,
        "days": day_time,
        "pre_req_raw": pre_req_str,
        "sections": sections,
    }


def get_dept_or_courses(dept: str = None) -> dict:
    soup = get_soup(dept)

    retDict = {}
    table_tag = soup.find("tbody").findChild()

    while table_tag:
        children = table_tag.findChildren()
        retDict[children[1].get_text(strip=True)] = children[2].get_text(strip=True)
        table_tag = table_tag.findNextSibling()

    return retDict


def scrape_dept_list(depts: list) -> dict:
    retDict = {}
    for dept in depts:
        retDict.update({dept: {}})
        courses = get_dept_or_courses(dept)
        for course in courses.keys():
            number = course.split()[1]
            retDict[dept].update({number: {"name": courses[course]}})
            retDict[dept][number].update(get_course_sections(dept, number))
            retDict[dept][number]["instructors"] = {}
            for section in retDict[dept][number]["sections"]:
                retDict[dept][number]["instructors"].update(
                    {section: get_course_instructors(dept, number, section)}
                )

    return retDict


if __name__ == "__main__":
    # test
    # print(get_course_instructors('CPSC', '100', '201'))
    # print(get_dept_or_courses('ADHE'))
    # print(scrape_dept_list(['ADHE'])['ADHE']['ADHE 329'])
    # pprint(get_course_sections('ACAM', 250))
    print(scrape_dept_list(['CPSC']))
    # print(get_course_sections('CPSC', 310))
    pass


"""
format for date time. a bit redundant but good for edge cases;
alternate way will be try some pythonic way to store day time
    {
        '002' : {'Tue':(14:00, 16:00),
                 'Wed':(14:00, 15:00)},
        '100' : {'Mon':(11:00, 12:00)
                 'Tue':(11:00, 12:00)}
    }
"""

"""
GOALS: JSON with foll. specs (not final)
{
    index: int,
    code: str,
    number: str,
    name: str,
    description: str,
    sections: list,
    time: dict, # {section: datetime} # how to store multiple timings for one section? e.g.ACAM 250
    pre_reqs: nested list and tuple,
    pre_reqs_str: str, # this will be the raw string to display on the page incase something goes wrong
    instructors: dict, # {section: list of instructors}
    credits: int,
    term: str, # e.g. 2024W1 (maybe?)
    mode: str/number, # mode of delivery(hybrid, in-person, online)
}
"""

"""
{
'CPSC': {
        '100': {
                'description': 'course decription on ssc'
                'name': 'Computational Thinking'
                'credits': 4
                'sections': ['101', '201']
                'days': {
                        '101': {'Fri': ('15:00', '16:00'),
                                'Mon': ('15:00', '16:00'),
                                'Wed': ('15:00', '16:00')},
                        '201': {'Fri': ('15:00', '16:00'),
                                'Mon': ('15:00', '16:00'),
                                'Wed': ('15:00', '16:00')}
                        },
                'pre_req_raw': html_tags
                'instructors': {'101': ['OLA, OLUWAKEMI'],
                                '201': ['OLA, OLUWAKEMI']}
                }
        }
}
"""

"""
NOTE: This is really pre-lim code, used as a proof of concept. might have to divide it
      into scraper and parser.
"""

"""
TODO:
- *parse pre-reqs tags to string
- *parse the pre-reqs string to data structure using legacy code
- edge case: when there is no pre-req str
- edge case: when there are different times(two rows for a section) for days in a section
- edge case: a lot in 'ADHE' like wow (esp sections like 63A etc)
- need fail safes
- test it for various edge cases
- test/check for webpage structures(all the findAll and index keeping might/might not work for every page)
* will take some time
"""
