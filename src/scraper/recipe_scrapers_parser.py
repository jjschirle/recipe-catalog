# recipe_scrapers_parser.py
# - use recipe-scrapers library
# - https://github.com/hhursev/recipe-scrapers

# src/scraper/recipe_scrapers_parser.py
from recipe_scrapers import scrape_me
from utils.ingredient import parse_and_clean_ingredients
from utils.text import clean_title

def parse_with_recipe_scrapers(url, debug=False):
    """
    Try to scrape a recipe using the recipe-scrapers library as fallback.
    Returns a dictionary or None if failed.
    """
    try:
        scraper = scrape_me(url)

        title = scraper.title() or "Untitled Recipe"
        title = clean_title(title)

        ingredients_detail = scraper.ingredients() or []
        instructions = scraper.instructions() or ""
        cuisine = []
        tags = scraper.tags() or [] if hasattr(scraper, "tags") else []
        servings = scraper.yields() or "N/A"
        prep_time = "N/A"
        video = ""

        ingredients_list = parse_and_clean_ingredients(ingredients_detail, debug=debug)
        dietary = []

        # recipe-scrapers usually does not provide nutrition
        nutrition_text = ""

        parsed = {
            "title": title,
            "ingredients_detail": ingredients_detail,
            "ingredients_list": ingredients_list,
            "instructions": instructions,
            "nutrition": nutrition_text,
            "cuisine": cuisine,
            "tags": tags,
            "dietary": dietary,
            "prep_time": prep_time,
            "servings": servings,
            "video": video,
        }

        return parsed

    except Exception as e:
        if debug:
            print(f"❌ recipe-scrapers failed: {e}")
        return None
