"""Web scraping utilities for HHSC/LBB public data."""

from pathlib import Path

import requests
from bs4 import BeautifulSoup

DATA_RAW = Path(__file__).parent.parent.parent / "data" / "raw"

# Common headers to avoid bot blocking on government sites
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


def download_file(url: str, filename: str, subdir: str = "") -> Path:
    """Download a file from URL to data/raw/.

    Args:
        url: Source URL
        filename: Name to save as
        subdir: Optional subdirectory within data/raw/
    """
    target_dir = DATA_RAW / subdir if subdir else DATA_RAW
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / filename

    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    target.write_bytes(response.content)
    return target


def fetch_page(url: str) -> BeautifulSoup:
    """Fetch a web page and return parsed BeautifulSoup."""
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def extract_tables_from_pdf(pdf_path: str | Path, pages: str = "all") -> list:
    """Extract tables from a PDF using tabula-py.

    Args:
        pdf_path: Path to PDF file
        pages: Page specification (e.g., "1", "1-3", "all")
    """
    import tabula

    return tabula.read_pdf(str(pdf_path), pages=pages, multiple_tables=True)
