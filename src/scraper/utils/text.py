# Slugify, title cleaning, general text helpers
import re
import html


def slugify(text):
    """
    Convert text to a URL-friendly slug:
    - Lowercase
    - Strip leading/trailing spaces
    - Replace spaces with hyphens
    """
    return text.lower().strip().replace(" ", "-")

def clean_title(text):
    """
    Decode HTML entities and remove possessive 's (e.g., "John's" -> "John").
    """
    if not isinstance(text, str):
        return ""

    # Decode HTML entities
    decoded = html.unescape(text)

    # Remove possessive 's
    # Matches words ending with 's or ’s (with typographic apostrophes too)
    cleaned = re.sub(r"(\b\w+)[’']s\b", r"\1", decoded)

    # Strip leading/trailing spaces
    return cleaned.strip()


def clean_ingredient_text(text):
    """
    Remove unwanted non-alphabetic characters from an ingredient string
    (except hyphens and %), lowercase it, and normalize spaces.
    """
    if not isinstance(text, str):
        return ""
    cleaned = re.sub(r"[^a-zA-Z\-%\s]", "", text)
    return re.sub(r"\s+", " ", cleaned).strip().lower()



