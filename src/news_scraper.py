from bs4 import BeautifulSoup
import requests
import pandas as pd


data = []

sitemap = "https://www.bbc.com/sitemaps/https-index-com-news.xml"

url = "https://www.bbc.com/news"

sitemap_reponse = requests.get(sitemap)

soup = BeautifulSoup(sitemap_reponse.content, "xml")

sitemaps = soup.find_all("loc")


for sitemap in sitemaps:
    url = sitemap.text
    reponse = requests.get(url)

    soup = BeautifulSoup(reponse.content, "xml")
    
    for news in soup.find_all("url"):
        
        news_url = news.find("loc").text
        news_name = news.find("news:name").text
        news_headline = news.find("news:title").text  
        news_summary = ""
        news_row = {
            "Name": news_name,
            "Headline": news_headline,
            "Summary": news_summary,
            "URL": news_url
        }
        data.append(news_row)

data = pd.DataFrame(data)

data.to_csv("data/headlines.csv", index = False)