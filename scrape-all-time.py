import requests

from bs4 import BeautifulSoup

URL = "https://www.xwordinfo.com/Popular"
FILE_PATH = "words-all-time.csv"
DATA = ["word,count"]


# Request the web page
def request_page(url):
    page = requests.get(url)
    html = BeautifulSoup(page.content, "html.parser")
    return html


# Grab each word and word count
def parse_table(html):

    # Pull the rows of the table, excluding the header
    rows = html.find_all("tr")[1:]
    for row in rows:
        c = int(row.find("td", class_="count").text)
        word_e = row.find("td", class_="words")
        for w in word_e.find_all("a"):

            # We only care about three and four letter words
            if len(w.text) > 4:
                continue

            line = "{},{}".format(w.text, c)
            DATA.append(line)

    return


if __name__ == "__main__":

    html = request_page(URL)
    parse_table(html)

    with open(FILE_PATH, "w") as f:
        text = "\n".join(DATA)
        f.write(text)