# ingestion/doi_ingestor.py
import os
import tempfile
from paperscraper.pdf import save_pdf
import urllib.request
import tarfile
import glob

def fetch_tex_by_doi(doi):
    # Create a temporary directory to store the downloaded TEX
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "article.tar.gz")
        try:
            # Attempt to save Zip File
            local_filename, _ = urllib.request.urlretrieve(f'https://arxiv.org/src/{doi}', filename=zip_path)

            # Extract Zip File
            tar = tarfile.open(local_filename, "r:gz")
            tar.extractall(tmpdir)
            tar.close()

            # Read main Tex file
            tex_files = glob.glob(os.path.join(tmpdir, "*.tex"))
            if not tex_files:
                raise FileNotFoundError("Error: No .tex files found in directory")
            if len(tex_files) > 1:
                print(f"Warning: Multiple .tex files found in directory. Reading the first one: {tex_files[0]}")

            with open(tex_files[0], "r", encoding="utf-8") as f:
                tex_content = f.read()
                return {
                    'type': 'tex',
                    'content': tex_content,
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
                'content': f"<html><body>Failed to retrieve Tex for {doi}. Error: {str(e)}</body></html>",
                'metadata': {
                    'doi': doi,
                    'source': 'doi_lookup'
                }
            }

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