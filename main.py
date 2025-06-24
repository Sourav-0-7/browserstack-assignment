from scraper.opinion_scraper import get_articles
from translator.translator import translate
from analyzer.text_analyzer import analyze
from dotenv import load_dotenv
load_dotenv()

def run_all():
    articles = get_articles()
    print("\n--- Scraped Articles (Spanish) ---")
    for art in articles:
        print(f"\nTitle: {art['title']}\nContent (first 200 chars):\n{art['content'][:200]}...\nImage URL: {art['img']}")

    translated = [translate(a["title"]) for a in articles]
    print("\n--- Translated Titles (English) ---")
    for t in translated:
        print(t)

    freqs = analyze(translated)
    print("\n--- Repeated Words (count > 2) ---")
    for w, c in freqs.items():
        print(f"{w}: {c}")

if __name__ == "__main__":
    run_all()
