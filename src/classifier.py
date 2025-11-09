# imports
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_article(headline, similar_headlines):
    developer_prompt = """
        You are a classifier that determines what news people get notified about. Your job is to
        evaluate a target article and depending on its content and given similar articles reported 
        in the past, classify it in one of the below 5 categories.

        1) Massive breaking news. Major development or original story.

        2) Normal breaking news. Major development or original story.

        3) Normal breaking news. Minor development.

        4) Non-breaking news. Original story, major development, or minor development.

        5) Duplicate news. This can be massive breaking news, normal breaking news, or 
        non-breaking news.

        Here are some definitions to help guide your classification:

        Massive breaking news: Huge news, requiring the immediate notification and attention of
        the people. This can be in the form of massive developments, or massive new events. This 
        is reserved for the few events and developments per year that has massive impact on the 
        lives of many/a majority people.

        Normal breaking news: Large events and developments that have a large impact and/or affect
        on the sentiment on the majority of the population. This news should warrant the attention of
        the people. Those who enjoy keeping an eye across major events and developments around the 
        world should be notified of this news. 

        Non-breaking news: News that is not significant enough to warrant the attention of the
        majority of people. 
        
        Duplicate news: This story has been reported already. This can be breaking or non-breaking
        news, but is redundant based on the previous similar articles given.

        Minor development: A continuation of a previous article, but with onyl minor udpates. No
        updates that warrant the attention attention of the people. Make sure under the "similar
        headlines", there is an article about the same topic, but at a different stage in development.

        Major development: A continutation of a previous article, but with major developments/
        additional information. Enough to warrant the attention of the people. Make sure that under
        the "similar headlines", there is an article about the same topic, but at a different
        stage in development.

        Original story: A brand new development and event that has not been reported before based
        on the similar articles given. Make sure that under the "similar headlines", there is no
        article that is about the same development/event.

        Be sure to use the similar given articles as a guide to determine whether the article is
        a duplicate, minor development, major development, or original story. Classify any articles
        that have already been seen before based on the past similar given articles as duplicate news.
        We do not want to notify users twice of the same information, unless there are major 
        developments, as we want to do everything in our power to prevent spam/overload of notifications.

        Output one number (integer), 1-5, that reflects the headline based on the 5 above categories.
    """

    similar_list = "\n".join([f"{i}. {h}" for i, h in enumerate(similar_headlines, 1)])

    user_prompt = f"""
        Target/Main Headline: 
        - {headline}

        Similar Headlines:
        {similar_list}
    """

    response = client.responses.create(
        model="gpt-5-nano",
        reasoning={"effort": "medium"},
        input=[
            {"role": "developer", "content": developer_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    classification = int(response.output_text.strip())
    return classification