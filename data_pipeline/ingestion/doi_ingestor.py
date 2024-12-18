# ingestion/doi_ingestor.py
import os
import tempfile
from paperscraper.pdf import save_pdf

def fetch_article_by_doi(doi):
    # Try to retrieve PDF directly using paperscraper
    paper_data = {'doi': doi}

    # Create a temporary directory to store the downloaded PDF
    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "article.pdf")
        try:
            # Attempt to save the PDF using paperscraper
            # This works best for arXiv and preprint servers supported by paperscraper
            saved = save_pdf(paper_data, filepath=pdf_path)
            if saved:
                # Read the PDF into memory
                with open(pdf_path, 'rb') as f:
                    pdf_content = f.read()
                return {
                    'type': 'pdf',
                    'content': pdf_content,
                    'metadata': {
                        'doi': doi,
                        'source': 'doi_lookup'
                    }
                }
            else:
                # If PDF not found or not supported, return a placeholder HTML content
                return {
                    'type': 'html',
                    'content': f"<html><body>No PDF found for {doi}</body></html>",
                    'metadata': {
                        'doi': doi,
                        'source': 'doi_lookup'
                    }
                }
        except Exception as e:
            # If an error occurs (e.g. unsupported DOI, rate limiting, paywall)
            # return a fallback HTML
            return {
                'type': 'html',
                'content': f"<html><body>Failed to retrieve PDF for {doi}. Error: {str(e)}</body></html>",
                'metadata': {
                    'doi': doi,
                    'source': 'doi_lookup'
                }
            }

def fetch_articles_by_dois(dois):
    articles = []
    for doi in dois:
        article = fetch_article_by_doi(doi)
        articles.append(article)
    return articles