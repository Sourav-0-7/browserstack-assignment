import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_articles(driver=None):
    close_driver = False
    if driver is None:
        options = Options()
        # options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        close_driver = True

    url = "https://elpais.com/opinion/"
    logging.info(f"Navigating to {url}")
    driver.get(url)
    time.sleep(3)  # Increased for mobile compatibility

    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles_data = []

    for idx, article in enumerate(soup.select("article")[:5]):
        title_tag = article.find("h2")
        link_tag = article.find("a", href=True)
        if not (title_tag and link_tag):
            logging.warning(f"Skipping article {idx}: Missing title or link")
            continue

        article_url = link_tag["href"]
        if article_url.startswith("/"):
            article_url = "https://elpais.com" + article_url
        logging.info(f"Navigating to article {idx}: {article_url}")
        driver.get(article_url)
        time.sleep(3)  # Increased for mobile compatibility

        page = BeautifulSoup(driver.page_source, "html.parser")
        content_tag = page.select_one("article")
        content = content_tag.get_text(separator=" ") if content_tag else "No content"

        img_tag = page.select_one("article img")
        img_url = img_tag["src"] if img_tag and img_tag.has_attr("src") else None

        # Pass browser_name to save_image
        browser_name = driver.capabilities.get("browserName", "unknown").lower()
        device_name = driver.capabilities.get("bstack:options", {}).get("deviceName", "")
        unique_id = device_name or browser_name
        img_path = save_image(img_url, idx, unique_id) if img_url else None

        articles_data.append({
            "title": title_tag.get_text().strip(),
            "content": content.strip(),
            "img": img_path
        })

    if close_driver:
        driver.quit()
    return articles_data

def save_image(url, idx, unique_id):
    try:
        os.makedirs("images", exist_ok=True)
        ext = url.split(".")[-1].split("?")[0]
        filename = f"images/article_{idx}_{unique_id}.{ext}"  # Unique filename per browser/device
        logging.info(f"Saving image to {filename}")
        resp = requests.get(url, timeout=5)
        if resp.ok:
            with open(filename, "wb") as f:
                f.write(resp.content)
            return filename
    except Exception as e:
        logging.error(f"[Image Error] {e}")
    return None