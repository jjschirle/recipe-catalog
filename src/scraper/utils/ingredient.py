# Ingredient-specific parsing & cleaning
import re
from ingredient_parser import parse_ingredient
import inflect
from .text import clean_ingredient_text

p = inflect.engine()


def split_compound_ingredients(ingredient):
    """
    Split ingredients joined by 'and' or '&' when it makes sense,
    e.g. 'salt and pepper' → ['salt', 'pepper']
    """
    # Basic check for ' and ' or ' & '
    if ' and ' in ingredient:
        parts = [part.strip() for part in ingredient.split(' and ')]
        # If both parts are short and simple, split
        if all(len(p.split()) <= 3 for p in parts):
            return parts
    elif ' & ' in ingredient:
        parts = [part.strip() for part in ingredient.split(' & ')]
        if all(len(p.split()) <= 3 for p in parts):
            return parts
    return [ingredient]

def is_section_header(text):
    """
    Heuristic to detect section headers (e.g., "for the dressing", "salad:").
    These are usually short lines containing keywords and not real ingredients.

    Returns True if text is a header, False otherwise.
    """
    text_lower = text.lower()
    keywords = ["for the", "dressing", "salad", "marinade", "sauce", "rub", "brine",
                "add-in", "garnish", "topping", "to serve", "to garnish", "for serving"]
    return any(kw in text_lower for kw in keywords) and len(text_lower.split()) <= 5

def strip_prep_descriptors(text):
    """
    Remove common preparation descriptors from ingredient names
    (e.g., "chopped", "grilled", "fresh") to get a canonical base name.
    """
    descriptors = [
        "grilled", "chopped", "minced", "cooked", "fresh", "sliced", "diced",
        "crushed", "peeled", "frozen", "roasted", "toasted", "ground",
        "small", "large", "medium", "ripe", "slightly", "raw", "natural",
        "creamy", "freshly", "optional", "plus", "cubed", "thinly", "fancy",
        "extra", "virgin", "pure", 'store', 'bought', 'fresh', 'torn'
    ]

    words = text.split()
    # Strip descriptors from start
    while words and words[0] in descriptors:
        words.pop(0)
    # Strip descriptors from end
    while words and words[-1] in descriptors:
        words.pop()
    return " ".join(words)


def singularize(text):
    """
    Singularize the last word in a string using the inflect library.
    Useful for converting "breasts" -> "breast" when tagging.
    """
    words = text.split()
    if not words:
        return text
    words[-1] = p.singular_noun(words[-1]) or words[-1]
    return " ".join(words)

def parse_and_clean_ingredients(ingredients_list, debug=False):
    """
    Parse and clean an ingredient list using ingredient-parser.

    Steps:
    - Skip section headers.
    - Use semantic parser to extract canonical ingredient name.
    - Clean characters and prep descriptors.
    - Singularize last word for consistent tagging.

    Parameters:
    - ingredients_list: List of ingredient strings.
    - debug: If True, prints step-by-step info.

    Returns:
    - List of cleaned ingredient names suitable for filtering and tags.
    """
    cleaned_list = []
    for ing in ingredients_list:
        if is_section_header(ing):
            if debug:
                print(f"🪄 Skipped section header: '{ing}'")
            continue
        try:
            # First, parse ingredient with the parser lib
            parsed = parse_ingredient(ing)
            raw_name = parsed.name[0].text if parsed.name else ing

            # Split alternatives separated by " or "
            alternatives = [alt.strip() for alt in raw_name.split(" or ") if alt.strip()]
            for alt in alternatives:
                # Clean descriptors and quantity leftover from parsing
                core = strip_prep_descriptors(alt)
                core = clean_ingredient_text(core)
                core = singularize(core)

                # Ignore empty or weird entries
                if core and core not in cleaned_list:
                    cleaned_list.append(core)
                    if debug:
                        print(f"🔬 Parsed ingredient: '{core}'")

        except Exception as e:
            if debug:
                print(f"⚠️ Parse error '{ing}': {e}")
            # Fallback fallback: just clean and singularize
            fallback_core = clean_ingredient_text(strip_prep_descriptors(ing))
            fallback_core = singularize(fallback_core)
            if fallback_core and fallback_core not in cleaned_list:
                cleaned_list.append(fallback_core)
    return cleaned_list