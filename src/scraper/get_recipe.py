# get_recipe.py
# - Holds the main function
# - Handles CLI args
# - Decides which parser to call

# src/scraper/get_recipe.py

import sys
import os
from extruct_parser import parse_with_extruct
from recipe_scrapers_parser import parse_with_recipe_scrapers
import globals
from utils import is_valid_url, slugify

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 get_recipe.py [URL] [--debug]")
        sys.exit(1)

    url = sys.argv[1]
    debug = False

    if len(sys.argv) >= 3 and sys.argv[2].lower() == "--true":
        debug = True

    if not is_valid_url(url, debug=debug):
        print("❌ Invalid or unreachable URL.")
        sys.exit(1)

    print(f"Fetching recipe from: {url}")

    # 1️⃣ Try extruct first
    data = parse_with_extruct(url, debug=debug)
    if data:
        print("✅ Successfully parsed with extruct!")
    else:
        print("⚠️ Extruct failed, trying recipe-scrapers fallback...")

        # 2️⃣ Try recipe-scrapers
        data = parse_with_recipe_scrapers(url, debug=debug)
        if data:
            print("✅ Successfully parsed with recipe-scrapers!")
        else:
            print("❌ All parsing methods failed. Consider adding custom BeautifulSoup fallback.")
            sys.exit(1)

    # Check required fields
    if not data.get("title") or not data.get("ingredients_list"):
        print("❌ Title and ingredients are required. Exiting.")
        sys.exit(1)

    # Build markdown frontmatter and content
    frontmatter = f"""---
title: "{data['title']}"
tags: {data.get('tags', [])}
cuisine: {data.get('cuisine', [])}
dietary: {data.get('dietary', [])}
allergy: {data.get('allergy', [])}
ingredients: {data.get('ingredients_list', [])}
prep_time: "{data.get('prep_time', 'N/A')}"
servings: "{data.get('servings', 'N/A')}"
source: "{url}"
video: "{data.get('video', '')}"
---

## Ingredients

"""
    ingredients_md = ''.join([f"- {ing}\n" for ing in data.get('ingredients_detail', [])])
    instructions_md = "\n## Instructions\n\n" + data.get('instructions', '')
    comments_md = "\n## Comments and Notes\n\nWrite your notes here..."

    content = frontmatter + ingredients_md + instructions_md + comments_md

    filename = slugify(data['title']) + ".md"
    filepath = os.path.join(globals.RECIPE_FOLDER, filename)

    # Ensure directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Recipe saved to {filepath}")

if __name__ == "__main__":
    main()
