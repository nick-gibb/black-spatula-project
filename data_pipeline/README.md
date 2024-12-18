# Data Pipeline for Scientific Article Ingestion and Processing

This is the pipeline for ingesting scientific articles (from APIs or web sources), parsing their content (PDF or HTML), processing the extracted text with OpenAI, and storing the results in a data store.

## Key Features

- **Ingestion**: Fetch articles from web APIs or directly via scraping given a DOI.
- **Parsing**: Extract text and figures from PDFs and HTML documents.
- **Processing**: Integrate with OpenAI APIs to derive structured insights.
- **Storage**: Save processed data into a storage backend like Google Sheets or AirTable.
