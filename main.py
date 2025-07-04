from bs4 import BeautifulSoup
from io import BytesIO
from pypdf import PdfReader, PdfWriter
import requests
from urllib.parse import urljoin

MAIN_URL = "https://nysedregents.org/"
MAIN_EXCLUDED_HREFS = [
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
SUBJECT_EXCLUDED_HREFS = {
    "https://nysedregents.org/algebratwo/": [
        "-annotations-",
        "ccrev.pdf",
        "cc.pdf",
        "ltexam.pdf",
        "examlt.pdf",
        "exam-lt.pdf",
    ]
}
SUBJECT_MULTIPLE_CHOICE_PHRASES = {
    "https://nysedregents.org/Chemistry/":
    "Record your answers in",
    "https://nysedregents.org/Physics/":
    "Record your answers in",
    "https://nysedregents.org/algebratwo/":
    "Answer all 8 questions in",
    "https://nysedregents.org/geometryre/":
    "Answer all 7 questions in",
    "https://nysedregents.org/ghg2/home.html":
    "These questions are based on the accompanying documents",
}
RATING_GUIDE_EXCLUDE_PAGE_PHRASES = {
    "Directions to the Teacher",
    "Teachers should become familiar with the",
    "Chart for Converting Total Test Raw Scores",
    "Map to Core Curriculum",
}
HREF_REPLACEMENTS = {
    "https://www.nysedregents.org/Physics/613/phys62012-rg.pdf":
    "https://www.nysedregents.org/Physics/613/phys62013-rg.pdf"
}


def get_valid_input(prompt, max_value):
    while True:
        try:
            user_input = int(input(prompt))
            if 1 <= user_input <= max_value:
                return user_input
            else:
                print(
                    "Invalid index. Please enter a number between 1 and %d." %
                    max_value)
        except ValueError:
            print("Invalid input. Please enter a number.")


def fetch_hrefs_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    anchor_tags = soup.find_all("a", href=True)
    hrefs = [
        tag["href"] for tag in anchor_tags
        if tag["href"] not in MAIN_EXCLUDED_HREFS
    ]
    return hrefs


def write_final_pdf():
    rating_guide_page = 0
    while rating_guide_page < len(rating_guide_pdf.pages):
        rating_guide_text = rating_guide_pdf.pages[
            rating_guide_page].extract_text()
        if not any(phrase in rating_guide_text
                   for phrase in RATING_GUIDE_EXCLUDE_PAGE_PHRASES):
            break
        rating_guide_page += 1

    last_rating_guide_page = len(rating_guide_pdf.pages) - 1
    while last_rating_guide_page >= 0:
        rating_guide_text = rating_guide_pdf.pages[
            last_rating_guide_page].extract_text()
        if not any(phrase in rating_guide_text
                   for phrase in RATING_GUIDE_EXCLUDE_PAGE_PHRASES):
            break
        last_rating_guide_page -= 1

    last_non_empty_exam_page = len(exam_pdf.pages) - 1
    while last_non_empty_exam_page >= 0:
        exam_page_text = exam_pdf.pages[last_non_empty_exam_page].extract_text(
        )
        if len(exam_page_text) > 0:
            break
        last_non_empty_exam_page -= 1

    multiple_choice_phrase = SUBJECT_MULTIPLE_CHOICE_PHRASES.get(selected_link)
    multiple_choice_section = True

    for exam_page_number, exam_page in enumerate(
        [page for page in exam_pdf.pages if len(page.extract_text()) > 64]):
        if len(exam_page.extract_text()) < 0:
            continue
        if (multiple_choice_phrase and
                exam_page.extract_text().find(multiple_choice_phrase) != -1):
            multiple_choice_section = False
        pdf_writer.add_page(exam_page)
        if exam_page_number <= 0:
            continue
        if multiple_choice_section:
            pdf_writer.add_page(scoring_key_pdf.pages[0])
        else:
            rating_guide_text = rating_guide_pdf.pages[
                rating_guide_page].extract_text()
            pdf_writer.add_page(rating_guide_pdf.pages[rating_guide_page])
            if rating_guide_page < last_rating_guide_page:
                rating_guide_page += 1
    if multiple_choice_phrase:
        if rating_guide_page <= last_rating_guide_page:
            for page in rating_guide_pdf.pages[rating_guide_page:]:
                pdf_writer.add_page(page)
    else:
        pdf_writer.append(rating_guide_pdf)


def get_yes_no_input(prompt, default=False):
    while True:
        user_input = input(prompt).lower()
        if user_input in ["y", "n", ""]:
            return user_input == "y" if user_input else default
        print(
            "Invalid input. Please enter 'y' or 'n' (or press Enter for default)"
        )


if __name__ == "__main__":
    links = [
        urljoin(MAIN_URL, href) for href in fetch_hrefs_from_url(MAIN_URL)
    ]
    for i, link in enumerate(links):
        print("%d. %s" % (i + 1, link))

    index = get_valid_input(
        "Enter the index of the link you want to select (1 to %d): " %
        len(links),
        len(links),
    )
    selected_link = links[index - 1]

    include_answers = get_yes_no_input(
        "Do you want to include scoring keys and rating guides? [Y/n] ", True)

    selected_hrefs = fetch_hrefs_from_url(selected_link)
    selected_pdfs = [
        HREF_REPLACEMENTS.get(href, href) for href in selected_hrefs
        if href.endswith(".pdf") and (
            selected_link not in SUBJECT_EXCLUDED_HREFS or not any(
                prefix in href
                for prefix in SUBJECT_EXCLUDED_HREFS[selected_link]))
    ]

    groups = {}

    for _, pdf_link in enumerate(selected_pdfs):
        identifier = "".join(s for s in pdf_link if s.isdigit())

        if identifier not in groups:
            groups[identifier] = []

        groups[identifier].append(pdf_link)

    pdf_writer = PdfWriter()
    for identifier, group in groups.items():
        exam_pdf_link = next(
            (string for string in group
             if (string.endswith("exam.pdf") or string.endswith("exam_w.pdf")
                 or string.endswith("exam611.pdf"))),
            None,
        )
        if not exam_pdf_link:
            continue
        exam_pdf_response = requests.get(urljoin(selected_link, exam_pdf_link))
        if exam_pdf_response.status_code != 200:
            continue
        exam_pdf = PdfReader(BytesIO(exam_pdf_response.content))

        if include_answers:
            scoring_key_pdf_link = next(
                (string for string in group if string.endswith("-sk.pdf")),
                None) or next(
                    (string
                     for string in group if (string.endswith("-rg.pdf")
                                             or string.endswith("-rgw.pdf"))),
                    None,
                )
            rating_guide_pdf_link = next(
                (string for string in group if
                 (string.endswith("-rg.pdf") or string.endswith("-rgw.pdf"))),
                None,
            )
            if not scoring_key_pdf_link or not rating_guide_pdf_link:
                continue

            scoring_key_pdf_response = requests.get(
                urljoin(selected_link, scoring_key_pdf_link))
            rating_guide_pdf_response = requests.get(
                urljoin(selected_link, rating_guide_pdf_link))
            if (scoring_key_pdf_response.status_code != 200
                    or rating_guide_pdf_response.status_code != 200):
                continue

            scoring_key_pdf = PdfReader(
                BytesIO(scoring_key_pdf_response.content))
            rating_guide_pdf = PdfReader(
                BytesIO(rating_guide_pdf_response.content))
            write_final_pdf()
        else:
            for page in exam_pdf.pages:
                pdf_writer.add_page(page)

    with open("final.pdf", "wb") as final_pdf:
        pdf_writer.write(final_pdf)
