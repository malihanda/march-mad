import requests

from bs4 import BeautifulSoup

URL = "https://www.xwordinfo.com/Popular?year={}"
FILE_PATH = "words.csv"
DATA = ["year,word,count"]


# Request the web page using the year-specific URL
def request_page(url):
    page = requests.get(url)
    html = BeautifulSoup(page.content, "html.parser")
    return html


# Return a list of (word, count) pairs
def parse_table(html, yr):

    # Pull the rows of the table, excluding the header
    rows = html.find_all("tr")[1:]
    for row in rows:
        c = int(row.find("td", class_="count").text)
        word_e = row.find("td", class_="words")
        for w in word_e.find_all("a"):

            # We only care about three and four letter words
            if len(w.text) > 4:
                continue

            line = "{},{},{}".format(yr, w.text, c)
            DATA.append(line)

    return


if __name__ == "__main__":

    for yr in range(1993, 2021):
        print("Parsing {}...".format(yr))
        url = URL.format(yr)
        html = request_page(url)
        parse_table(html, yr)

    with open(FILE_PATH, "w") as f:
        text = "\n".join(DATA)
        f.write(text)