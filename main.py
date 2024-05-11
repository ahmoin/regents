import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

MAIN_URL = "https://nysedregents.org/"
EXCLUDED_HREFS = [
    "http://www.nysed.gov/",
    "#content_column",
    "http://www.nysed.gov/state-assessment",
    "http://www.nysed.gov/about/program-offices",
    "http://www.nysed.gov/curriculum-instruction",
    "http://www.nysed.gov/state-assessment",
    "https://www.nysedregents.org/",
    "elementary-intermediate.html",
    "loteslp/home.html",
    "http://www.nysed.gov/state-assessment/testing-materials-duplication-schools",
    "regents_lang.html",
    "translatedexams.html",
    "engageny/home.html",
    "http://www.nysl.nysed.gov/regentsexams.htm",
    "ComprehensiveEnglish/",
    "IntegratedAlgebra/",
    "Geometry/",
    "a2trig/home.html",
    "MathematicsB/",
    "USHistoryGov/home.html",
    "transitionghg10/home.html",
    "GlobalHistoryGeography/",
    "archive-regents.html",
    "http://www.nysed.gov/state-assessment/contact-information",
    "http://www.nysed.gov/contact-NYSED",
    "http://www.nysed.gov/about/index-a-z/",
    "http://www.nysed.gov/terms-of-use#Accessibility",
    "http://www.nysed.gov/terms-of-use",
]

response = requests.get(MAIN_URL)
soup = BeautifulSoup(response.text, "html.parser")
anchor_tags = soup.find_all("a", href=True)
hrefs = [tag["href"] for tag in anchor_tags if tag["href"] not in EXCLUDED_HREFS]

links = [urljoin(MAIN_URL, href) for href in hrefs]

print(links)
