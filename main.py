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


def get_valid_input(prompt, max_value):
    while True:
        try:
            index = int(input(prompt))
            if 1 <= index <= max_value:
                return index
            else:
                print(
                    "Invalid index. Please enter a number between 1 and %d." % max_value
                )
        except ValueError:
            print("Invalid input. Please enter a number.")


def fetch_links_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    anchor_tags = soup.find_all("a", href=True)
    hrefs = [tag["href"] for tag in anchor_tags if tag["href"] not in EXCLUDED_HREFS]
    return hrefs


def main():
    links = [urljoin(MAIN_URL, href) for href in fetch_links_from_url(MAIN_URL)]
    for i, link in enumerate(links):
        print("%d. %s" % (i + 1, link))

    index = get_valid_input(
        "Enter the index of the link you want to select (1 to %d): " % len(links),
        len(links),
    )
    selected_link = links[index - 1]
    selected_urls = fetch_links_from_url(selected_link)
    selected_pdfs = [
        link.split("/")[-1] for link in selected_urls if link.endswith(".pdf")
    ]
    groups = {}

    for _, pdf_link in enumerate(selected_pdfs):
        identifier = "".join(s for s in pdf_link if s.isdigit())

        if identifier not in groups:
            groups[identifier] = []

        groups[identifier].append(pdf_link)

    for key, value in groups.items():
        print(key, ":", value)


if __name__ == "__main__":
    main()
