# This file handles data loading and index creation, which are needed before search.

import requests # loads HTTP library so you can fetch URLs
from minsearch import Index # imports search index class

# Define load_faq_data function (fetches documents / loads the data)
# This function is reusable and takes no arguments 
def load_faq_data():
    docs_url = "https://datatalks.club/faq/json/courses.json"
    response = requests.get(docs_url) #fetches the docs_url
    courses_raw = response.json() #parses response from raw text to Python list of course objects

    documents = [] #empty list to accumulate all FAQ documents across all courses
    url_prefix = "https://datatalks.club/faq" #base URL to get combined with each course path

    for course in courses_raw:
        course_url = f"""{url_prefix}{course["path"]}""" #builds the full URL
        course_response = requests.get(course_url) #fetches course_url data
        course_response.raise_for_status() #throws an error if request failed
        course_data = course_response.json() #parses response into a Python list

        documents.extend(course_data) #Adds all docs from the course into the master list. Then .extend flattens them in

    return documents #returns completed list to whoever calls the function

# Define build_index (creates a minsearch Index, specifying which fields to full-text search
# and which to use for exact filtering)
def build_index(documents):
    index = Index(
        text_fields=["question", "section", "answer"], #searchable by relevance. Get tokenized and scored by relevance when you run a query.
        keyword_fields=["course"] #filter by exact value
    )
    index.fit(documents) #Load all docs into the index and build the internal search structures
    return index #return the populated index, ready to accept search queries
