# URL checks, domain extraction
import re
import requests
from urllib.parse import urlparse


def is_valid_url(url, debug=False):
    """
    Check if a URL is syntactically valid and reachable.

    - Uses a regex to validate structure.
    - Adds a User-Agent header to mimic a browser and avoid bot blocks.
    - Prints debug info if enabled.

    Returns True if reachable (status code < 400), False otherwise.
    """
    regex = re.compile(r'^(?:http|ftp)s?://\S+$', re.IGNORECASE)

    if not re.match(regex, url):
        if debug:
            print("⚠️ Regex check failed for URL.")
        return False

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        if debug:
            print(f"🔎 Trying GET request to: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        if debug:
            print(f"🔎 Response status code: {response.status_code}")
        return response.status_code < 400
    except requests.RequestException as e:
        if debug:
            print(f"⚠️ GET request exception: {e}")
        return False

def extract_domain_tag(url):
    """
    Extract a simplified domain to use as a tag, e.g.,
    'www.allrecipes.com' => 'allrecipes'
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    if domain.endswith(".com"):
        domain = domain[:-4]
    if domain.endswith(".blogspot"):
        domain = domain[:-9]
    domain = domain.replace(".", "")
    return domain
