# src/scraper/extruct_parser.py
import requests
import extruct
from w3lib.html import get_base_url
from utils.ingredient import parse_and_clean_ingredients
from utils.text import clean_title

def parse_with_extruct(url, debug=False):
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        html = r.text
        base_url = get_base_url(r.text, r.url)

        data = extruct.extract(html, base_url=base_url, syntaxes=['json-ld'])
        json_ld = data.get('json-ld', [])

        recipe_data = None

        for item in json_ld:
            if item.get('@type') == 'Recipe' or ('@type' in item and 'Recipe' in item['@type']):
                recipe_data = item
                break

        if not recipe_data:
            if debug:
                print("⚠️ No JSON-LD recipe data found.")
            return None

        title = recipe_data.get("name", "Untitled Recipe")
        title = clean_title(title)

        ingredients_detail = recipe_data.get("recipeIngredient", [])
        instructions_raw = recipe_data.get("recipeInstructions", [])

        if isinstance(instructions_raw, list):
            instructions = "\n".join(
                [step.get("text", "") if isinstance(step, dict) else str(step) for step in instructions_raw]
            )
        else:
            instructions = str(instructions_raw)

        cuisine = recipe_data.get("recipeCuisine", [])
        if isinstance(cuisine, str):
            cuisine = [c.strip() for c in cuisine.split(",") if c.strip()]

        keywords = recipe_data.get("keywords", "")
        tags = [tag.strip() for tag in keywords.split(",")] if keywords else []

        prep_time = recipe_data.get("totalTime", "N/A")
        servings = recipe_data.get("recipeYield", "N/A")
        video_link = ""

        video_obj = recipe_data.get("video", None)
        if isinstance(video_obj, dict):
            video_link = video_obj.get("contentUrl", "")
        elif isinstance(video_obj, str):
            video_link = video_obj

        dietary = [tag for tag in tags if tag.lower() in ["vegan", "vegetarian", "gluten-free", "dairy-free"]]
        ingredients_list = parse_and_clean_ingredients(ingredients_detail, debug=debug)

        # Nutrition parsing
        nutrition_data = recipe_data.get("nutrition", {})
        nutrition_text = ""
        if nutrition_data:
            nutrition_parts = []
            for key, value in nutrition_data.items():
                if key.startswith("@"):
                    continue
                nutrition_parts.append(f"{key.capitalize()}: {value}")
            nutrition_text = "\n".join(nutrition_parts)

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
            "video": video_link,
        }

        return parsed

    except Exception as e:
        if debug:
            print(f"Extruct parsing failed: {e}")
        return None
