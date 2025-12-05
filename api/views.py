import requests
from bs4 import BeautifulSoup
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def bbc_tech_latest(request):
    url = "https://www.bbc.com/news/technology"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_list = []

    #BBC h3 tags with links
    for item in soup.select("h3 a"):
        title = item.get_text(strip=True)
        href = item.get("href")

        if title and href and href.startswith("/news"):
            link = "https://www.bbc.com" + href
            news_list.append({"title": title, "link": link})

    #article tags
    if not news_list:
        for article in soup.find_all("article"):
            a = article.find("a")
            if a and a.get("href"):
                title = a.get_text(strip=True)
                href = a.get("href")
                if title:
                    link = "https://www.bbc.com" + href
                    news_list.append({"title": title, "link": link})

    #any <a> that contains "technology"
    if not news_list:
        for a in soup.find_all("a"):
            title = a.get_text(strip=True)
            href = a.get("href", "")
            if "technology" in href and title:
                link = "https://www.bbc.com" + href
                news_list.append({"title": title, "link": link})

    return Response({
        "count": len(news_list),
        "news": news_list
    })
