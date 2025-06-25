import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def get_articles():
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    url = "https://elpais.com/opinion/"
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles_data = []

    for idx, article in enumerate(soup.select("article")[:5]):
        title_tag = article.find("h2")
        link_tag = article.find("a", href=True)
        if not (title_tag and link_tag): continue

        article_url = link_tag["href"]
        if article_url.startswith("/"):
            article_url = "https://elpais.com" + article_url
        driver.get(article_url)
        time.sleep(2)

        page = BeautifulSoup(driver.page_source, "html.parser")
        content_tag = page.select_one("article")
        content = content_tag.get_text(separator=" ") if content_tag else "No content"

        img_tag = page.select_one("article img")
        img_url = img_tag["src"] if img_tag and img_tag.has_attr("src") else None

        img_path = save_image(img_url, idx) if img_url else None

        articles_data.append({
            "title": title_tag.get_text().strip(),
            "content": content.strip(),
            "img": img_path
        })

    driver.quit()
    return articles_data

def save_image(url, idx):
    try:
        os.makedirs("images", exist_ok=True)
        ext = url.split(".")[-1].split("?")[0]
        filename = f"images/article_{idx}.{ext}"
        resp = requests.get(url, timeout=5)
        if resp.ok:
            with open(filename, "wb") as f:
                f.write(resp.content)
            return filename
    except Exception as e:
        print(f"[Image Error] {e}")
    return None
