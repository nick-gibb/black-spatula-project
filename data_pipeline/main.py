# main.py
from ingestion.api_ingestor import fetch_articles_from_api
from ingestion.web_scraper import scrape_web_articles
from parsing.pdf_parser import parse_pdf
from parsing.html_parser import parse_html
from processing.openai_processor import process_with_openai
from storage.google_sheets_storage import store_results_in_sheets
from utils.logging_util import get_logger

logger = get_logger(__name__)

def run_pipeline():
    # Step 1: Ingestion
    logger.info("Starting ingestion...")
    api_articles = fetch_articles_from_api()  # Returns a list of { 'type': 'pdf' or 'html', 'content': <binary or raw> }
    web_articles = scrape_web_articles()      # Returns a similar list of article content

    # Combine all articles
    all_articles = api_articles + web_articles
    logger.info(f"Ingested {len(all_articles)} articles")

    # Step 2: Parsing
    logger.info("Parsing articles...")
    parsed_articles = []
    for article in all_articles:
        if article.get('type') == 'pdf':
            text, figures = parse_pdf(article['content'])
        else:
            text, figures = parse_html(article['content'])
        parsed_articles.append({
            'text': text,
            'figures': figures,
            'metadata': article.get('metadata', {})
        })

    # Step 3: Processing (OpenAI)
    # For now, we just simulate this step
    logger.info("Processing articles with OpenAI...")
    processed_results = []
    for parsed_article in parsed_articles:
        # This function would call OpenAI, but we’ll just pass through for now.
        result = process_with_openai(parsed_article['text'], parsed_article['figures'])
        processed_results.append(result)

    # Step 4: Storage
    logger.info("Storing results...")
    store_results_in_sheets(processed_results)
    logger.info("Pipeline completed.")

if __name__ == "__main__":
    run_pipeline()