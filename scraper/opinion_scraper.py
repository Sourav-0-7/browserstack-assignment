import os
import requests
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
def get_articles():
    os.makedirs('images', exist_ok=True)
    driver = webdriver.Chrome()
    driver.get("https://elpais.com/opinion/")

    # Step 1: Extract the first 5 article URLs
    article_elements = driver.find_elements(By.CSS_SELECTOR, "article a")[:5]
    article_urls = [a.get_attribute("href") for a in article_elements]

    results = []

    for idx, url in enumerate(article_urls, 1):
        driver.get(url)
        try:
            title = driver.find_element(By.TAG_NAME, "h1").text
            paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.a_c a_p") or \
                         driver.find_elements(By.CSS_SELECTOR, "div[data-testid='article-body'] p")
            content = "\n".join([p.text for p in paragraphs])

            img_url = None
            try:
                img_url = driver.find_element(By.TAG_NAME, "figure img").get_attribute("src")
                img_data = requests.get(img_url).content
                with open(f'images/article_{idx}.jpg', 'wb') as f:
                    f.write(img_data)
            except Exception:
                pass

            results.append({
                "title": title,
                "content": content,
                "img": img_url
            })
        except Exception as e:
            print(f"Failed to parse article: {url}, error: {e}")

    driver.quit()
    return results
