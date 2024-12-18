# main.py
import argparse
from utils.logging_util import get_logger
from ingestion.doi_ingestor import fetch_articles_by_dois
from parsing.pdf_parser import parse_pdf
from parsing.html_parser import parse_html
from processing.openai_processor import process_with_openai
from storage.google_sheets_storage import store_results_in_sheets

logger = get_logger(__name__)

def run_pipeline(dois=None, mode="default"):
    # Step 1: Ingestion
    if dois:
        logger.info(f"Ingesting articles by DOIs: {dois}")
        all_articles = fetch_articles_by_dois(dois)
    else:
        logger.info("No DOIs provided. Please provide DOIs to test ingestion.")
        all_articles = []

    logger.info(f"Ingested {len(all_articles)} articles.")

    # Step 2: Parsing
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

    # Step 3: Processing (OpenAI) - currently placeholder
    processed_results = []
    for parsed_article in parsed_articles:
        result = process_with_openai(parsed_article['text'], parsed_article['figures'])
        processed_results.append(result)

    # Step 4: Storage
    store_results_in_sheets(processed_results)
    logger.info("Pipeline completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the data pipeline")
    parser.add_argument("--doi", action="append", help="Specify one or more DOIs to ingest.")
    parser.add_argument("--mode", default="default", help="Mode of operation (e.g., 'default', 'test', 'fast').")
    args = parser.parse_args()

    run_pipeline(dois=args.doi, mode=args.mode)