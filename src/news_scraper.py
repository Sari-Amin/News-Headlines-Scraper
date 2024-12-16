from bs4 import BeautifulSoup
import requests
import pandas as pd

data = []

url = "https://www.bbc.com/news"

try:
    response = requests.get(url)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    exit(1)

soup = BeautifulSoup(response.content, "html.parser")

article = soup.find("article")

if article:
    news = article.find_all("a", class_ = "sc-2e6baa30-0 gILusN")

    for new in news:
        newsUrl = new.get("href")

        if newsUrl.startswith("/"):
            newsUrl = "https://www.bbc.com" + newsUrl

            newsHeadline = new.get_text()

            try:
                newsResponse = requests.get(newsUrl)
                newsResponse.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while fetching {newsUrl}: {e}")
                continue

            newsSoup = BeautifulSoup(newsResponse.content, "html.parser")
            newsSummary = newsSoup.find('meta', {"name": "description"})

            newsSummary = newsSummary["content"] if newsSummary else "No summary available."

            newRow = {
                "Headline" : newsHeadline,
                "Summary" : newsSummary,
                "Url" : newsUrl
            }

            data.append(newRow)

data = pd.DataFrame(data)

data.to_csv("data/headlines.csv", index = False)