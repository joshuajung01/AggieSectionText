import requests
import json
from typing import Dict, List
from dataSearch import *

def request_terms():
    """Performs a GET request for all terms in TAMU history"""
    url = "https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/classSearch/getTerms?dataType=json&offset=1&max=500"
    response = requests.get(url)
    return json.loads(response.content)


def post_term(term_code: str):
    """Makes a POST request to set the desired term for consequent requests. Returns cookies"""
    url = "https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/term/search?mode=courseSearch"
    body = {
        "dataType": "json",
        "term": term_code
    }
    response = requests.post(url, data=body)
    return response.cookies

def request_sections(dept: str, course_num: str, cookies):
    url = f"https://compassxe-ssb.tamu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults?txt_subjectcoursecombo={str(dept)+str(course_num)}&txt_term=202011&pageOffset=0&pageMaxSize=500&sortColumn=subjectDescription&sortDirection=asc"
    response = requests.get(url, cookies=cookies)
    return json.loads(response.content)

def search(dept: str, course_num: str, sec: str):
    name = str(dept) + " " + str(course_num) + " " + str(sec)

    terms = request_terms()
    term_code = terms[0]["code"]

    term_cookies = post_term(term_code)

    database = request_sections(dept,course_num,term_cookies)

    # pprint(database)
    if database["tamuActualTotal"] == 0:
        print('INVALID INPUT')
        return False

    # pprint(database)
    allsecs = find_all_class(database, dept, course_num)
    avasecs = find_avai_class(database, dept, course_num)
    if name in avasecs:
        return True
    elif name in allsecs:
        return False
    else:
        return False
