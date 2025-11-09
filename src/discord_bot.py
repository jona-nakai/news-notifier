from dotenv import load_dotenv
import os
import requests

load_dotenv()

WEBHOOK_URL_BREAKING = os.getenv("DISCORD_WEBHOOK_BREAKING")
ROLE_ID_BREAKING = os.getenv("DISCORD_ROLE_BREAKING")

WEBHOOK_URL_SEMI_BREAKING = os.getenv("DISCORD_WEBHOOK_SEMI_BREAKING")
ROLE_ID_SEMI_BREAKING = os.getenv("DISCORD_ROLE_SEMI_BREAKING")

WEBHOOK_URL_NON_BREAKING = os.getenv("DISCORD_WEBHOOK_NON_BREAKING")
ROLE_ID_NON_BREAKING = os.getenv("DISCORD_ROLE_NON_BREAKING")

news_type_dict = {
    "breaking": (WEBHOOK_URL_BREAKING, ROLE_ID_BREAKING),
    "semi-breaking": (WEBHOOK_URL_SEMI_BREAKING, ROLE_ID_SEMI_BREAKING),
    "non-breaking": (WEBHOOK_URL_NON_BREAKING, ROLE_ID_NON_BREAKING)
}

def send_news(headline, article_link, news_type):
    message = f"[**{headline}**]({article_link}) <@&{news_type_dict[news_type][1]}>"
    data = {"content": message}
    response = requests.post(news_type_dict[news_type][0], json=data)

    if response.status_code not in [200, 204]:
        print(f"Failed to send Discord message: {response.status_code}")