import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_articles():
    os.makedirs('images', exist_ok=True)
    driver = webdriver.Chrome()
    driver.get("https://elpais.com/opinion/")
    articles = driver.find_elements(By.CSS_SELECTOR, "article")[:5]
    result = []

    for idx, art in enumerate(articles, 1):
        link = art.find_element(By.TAG_NAME, "a").get_attribute("href")
        driver.get(link)
        title = driver.find_element(By.TAG_NAME, "h1").text
        paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.a_c a_p") or \
                     driver.find_elements(By.CSS_SELECTOR, "div[data-testid='article-body'] p")
        content = "\n".join([p.text for p in paragraphs])
        img_url = None
        try:
            img_url = driver.find_element(By.TAG_NAME, "figure img").get_attribute("src")
            img_data = requests.get(img_url).content
            fname = f"images/article_{idx}.jpg"
            with open(fname, "wb") as f: f.write(img_data)
        except Exception:
            pass

        result.append({"title": title, "content": content, "img": img_url})
        driver.back()

    driver.quit()
    return result
