import requests
import os
from dotenv import load_dotenv, find_dotenv

def grobid_parse_pdf(pdf_file: bytes):
    """
    Parses a PDF file using the GROBID service.

    Args:
        pdf_file (bytes): The PDF file to be parsed.

    Returns:
        str: The extracted XML from the GROBID service response.
    """
    # get from env
    load_dotenv(find_dotenv())
    grobid_url = os.environ.get("GROBID_URL")
    url = f"{grobid_url}/api/processFulltextDocument"
    files = {"input": pdf_file}
    response = requests.post(url, files=files)
    response.raise_for_status()
    return response