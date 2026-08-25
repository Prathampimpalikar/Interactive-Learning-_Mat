import json
import os

# Exact verified real models that exist in model/
REAL_ANIMAL_MODELS = {
    "Alligator": "Alligator.glb",
    "Ant": "ant.glb",
    "Red Ant": "redant.glb",
    "Alpaca": "alpaca.glb",
    "Asiatic Lion": "lion.glb",
    "Lion": "lion.glb",
    "Asiatic Elephant": "elephant.glb",
    "Elephant": "elephant.glb",
    "Bear": "Bear.glb",
    "Bee": "Bee.glb",
    "Buffalo": "Buffalo.glb",
    "Water Buffalo": "Buffalo.glb",
    "Camel": "Camel.glb",
    "Cat": "Cat.glb",
    "Cow": "Cow.glb"
}

REAL_FRUIT_MODELS = {
    "Apple": "Apple.glb",
    "Avocado": "Avocado.glb",
    "Banana": "banana.glb",
    "Elaichi Banana": "banana.glb",
    "Blackberry": "blackberry.glb",
    "Blueberry": "blueberry.glb",
    "Cherry": "Cherry.glb",
    "Coconut": "Coconut.glb"
}

REAL_NUMBER_MODELS = {
    "0": "0.glb",
    "1": "1.glb",
    "2": "2.glb",
    "3": "3.glb",
    "4": "4.glb",
    "5": "5.glb",
    "6": "6.glb",
    "7": "7.glb",
    "8": "8.glb",
    "9": "9.glb",
    "10": "10.glb"
}

# Read current dataset_full.json
with open("c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/dataset_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for a in data.get("animals", []):
    name = a.get("name", "").split(" (")[0].strip()
    matched_model = None
    for k, v in REAL_ANIMAL_MODELS.items():
        if k.lower() == name.lower() or k.lower() in name.lower():
            matched_model = v
            break
    if matched_model:
        a["model"] = matched_model
        a["hasRealModel"] = True
    else:
        a["model"] = None
        a["hasRealModel"] = False

for fr in data.get("fruits", []):
    name = fr.get("name", "").split(" (")[0].strip()
    matched_model = None
    for k, v in REAL_FRUIT_MODELS.items():
        if k.lower() == name.lower() or k.lower() in name.lower():
            matched_model = v
            break
    if matched_model:
        fr["model"] = matched_model
        fr["hasRealModel"] = True
    else:
        fr["model"] = None
        fr["hasRealModel"] = False

for n in data.get("numbers", []):
    num_str = str(n.get("number", ""))
    if num_str in REAL_NUMBER_MODELS:
        n["model"] = REAL_NUMBER_MODELS[num_str]
        n["hasRealModel"] = True

# Write back dataset_full.json
with open("c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/dataset_full.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

# Write back js/data.js
with open("c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/js/data.js", "w", encoding="utf-8") as f:
    f.write("const ALPHAMAT_DATA = " + json.dumps(data, indent=2) + ";\n")

print("Dataset updated: Only exact matching specimens have hasRealModel: true, all others will display AlphaMat company logo!")
