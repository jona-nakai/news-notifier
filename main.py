# imports
from src.ingest_news import get_feeds, parse_feed
from src.embeddings import embed_article_headline
from src.vector_database import init_db, is_new_article, store_article, return_similar_articles
from src.classifier import classify_article
from src.discord_bot import send_news

def main():
    RSS_urls = {
        "Reuters (via Google News)": "https://news.google.com/rss/search?q=site%3Areuters.com&hl=en-US&gl=US&ceid=US%3Aen",
        "AP News (via Google News)": "https://news.google.com/rss/search?q=site%3Aapnews.com&hl=en-US&gl=US&ceid=US%3Aen"
    }

    print("Retrieving RSS feeds")
    RSS_feeds = get_feeds(RSS_urls)
    feed_list = parse_feed(RSS_feeds)

    collection = init_db(path="data/chromadb")

    print("Finding new articles")
    new_articles = list()
    for article in feed_list:
        if is_new_article(collection=collection, article_id=article["id"]):
            new_articles.append(article)
    print(f'Found {len(new_articles)} new articles')
    
    for new_article in new_articles:
        embedding = embed_article_headline(new_article["title"])
        similar_articles = return_similar_articles(collection=collection, embedding=embedding)
        similar_headlines = [article["title"] for article in similar_articles]
        classification = classify_article(headline=new_article["title"], similar_headlines=similar_headlines)
        if classification == 1:
            print(f'Massive Breaking News: {new_article["title"]}')
            send_news(new_article["title"], f'<{new_article["link"]}>', "breaking")
        elif classification == 2:
            print(f'Breaking News: {new_article["title"]}')
            send_news(new_article["title"], f'<{new_article["link"]}>', "semi-breaking")
        elif classification == 3:
            print(f'__Breaking news, minor development: {new_article["title"]}')
        elif classification == 4:
            print(f'__Non-breaking news, minor development: {new_article["title"]}')
            send_news(new_article["title"], f'<{new_article["link"]}>', "non-breaking")
        elif classification == 5:
            print(f'__Duplicate News: {new_article["title"]}')
        else:
            print("[Classification Error]")
        
        new_article_dict = new_article.copy()
        new_article_dict["embedding"] = embedding
        new_article_dict["source"] = new_article["source"]["title"]
        new_article_dict["published_at"] = new_article["published_at"]
        store_article(collection=collection, article_dict=new_article_dict)

    all_articles = collection.get()
    feed_ids = set(article["id"] for article in feed_list)

    articles_to_delete = list()
    for id in all_articles["ids"]:
        if id not in feed_ids:
            articles_to_delete.append(id)
    
    if articles_to_delete:
        collection.delete(ids=articles_to_delete)

    if len(articles_to_delete) == 1:
        print(f'Deleted {len(articles_to_delete)} old article')
    else:
        print(f'Deleted {len(articles_to_delete)} old articles')

if __name__ == "__main__":
    main()