# recipe_scrapers_parser.py
# - use recipe-scrapers library
# - https://github.com/hhursev/recipe-scrapers

# src/scraper/recipe_scrapers_parser.py
from recipe_scrapers import scrape_me
from utils import parse_and_clean_ingredients

def parse_with_recipe_scrapers(url, debug=False):
    """
    Try to scrape a recipe using the recipe-scrapers library as fallback.
    Returns a dictionary or None if failed.
    """
    try:
        # scrape_html( html: str | None, org_url: str, *, online: bool = False, supported_only: bool | None = None, wild_mode: bool | None = None, )
        # scraper = scrape_me(url, wild_mode=True) does not have wild_mode
        scraper = scrape_me(url)

        title = scraper.title() or "Untitled Recipe"
        ingredients_detail = scraper.ingredients() or []
        instructions = scraper.instructions() or ""
        cuisine = []
        tags = scraper.tags() or [] if hasattr(scraper, "tags") else []
        servings = scraper.yields() or "N/A"
        prep_time = "N/A"
        video = ""

        # ingredients_list = [ing.split(",")[0].strip().split(" ")[-1] for ing in ingredients_detail if ing]
        ingredients_list = parse_and_clean_ingredients(ingredients_detail, debug=debug)
        dietary = []

        parsed = {
            "title": title,
            "ingredients_detail": ingredients_detail,
            "ingredients_list": ingredients_list,
            "instructions": instructions,
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
