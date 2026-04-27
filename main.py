from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Onsight Nutrition API",
    version="0.1.0"
)

FOODS = {
    "salmon_baked": {
        "display_name": "Salmon, baked",
        "density_g_ml": 1.00,
        "nutrients_100g": {
            "energy_kcal": 232,
            "protein_g": 25.2,
            "fat_g": 14.6,
            "carbohydrate_g": 0.0
        }
    },
    "chicken_breast_grilled": {
        "display_name": "Chicken breast, grilled",
        "density_g_ml": 1.15,
        "nutrients_100g": {
            "energy_kcal": 148,
            "protein_g": 32.0,
            "fat_g": 2.2,
            "carbohydrate_g": 0.0
        }
    },
    "olive_oil": {
        "display_name": "Olive oil",
        "density_g_ml": 0.92,
        "nutrients_100g": {
            "energy_kcal": 899,
            "protein_g": 0.0,
            "fat_g": 99.9,
            "carbohydrate_g": 0.0
        }
    },
    "spinach_raw": {
        "display_name": "Spinach, raw",
        "density_g_ml": 0.08,
        "nutrients_100g": {
            "energy_kcal": 16,
            "protein_g": 2.6,
            "fat_g": 0.6,
            "carbohydrate_g": 0.2
        }
    }
}


@app.get("/")
def root():
    return {"message": "Onsight Nutrition API is running"}


@app.get("/foods/search")
def search_foods(q: str):
    q_lower = q.lower()
    results = []

    for food_id, food in FOODS.items():
        if q_lower in food["display_name"].lower() or q_lower in food_id:
            results.append({
                "food_id": food_id,
                "display_name": food["display_name"]
            })

    return {
        "query": q,
        "results": results
    }


@app.get("/foods/{food_id}")
def get_food(food_id: str):
    food = FOODS.get(food_id)

    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    return {
        "food_id": food_id,
        **food
    }


@app.get("/foods/{food_id}/nutrition")
def get_nutrition_by_mass(food_id: str, mass_g: float):
    food = FOODS.get(food_id)

    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    nutrition = {}

    for nutrient_id, amount_100g in food["nutrients_100g"].items():
        nutrition[nutrient_id] = round(mass_g * amount_100g / 100, 2)

    return {
        "food_id": food_id,
        "display_name": food["display_name"],
        "mass_g": mass_g,
        "nutrition": nutrition,
        "calculation": "nutrient = mass_g × nutrient_per_100g / 100"
    }


@app.get("/foods/{food_id}/nutrition-from-volume")
def get_nutrition_by_volume(food_id: str, volume_ml: float):
    food = FOODS.get(food_id)

    if not food:
        raise HTTPException(status_code=404, detail="Food not found")

    density = food["density_g_ml"]
    mass_g = volume_ml * density

    nutrition = {}

    for nutrient_id, amount_100g in food["nutrients_100g"].items():
        nutrition[nutrient_id] = round(mass_g * amount_100g / 100, 2)

    return {
        "food_id": food_id,
        "display_name": food["display_name"],
        "volume_ml": volume_ml,
        "density_g_ml": density,
        "estimated_mass_g": round(mass_g, 2),
        "nutrition": nutrition,
        "calculation": "mass_g = volume_ml × density_g_ml; nutrient = mass_g × nutrient_per_100g / 100"
    }
