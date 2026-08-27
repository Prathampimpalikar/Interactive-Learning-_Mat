import json
import os
import re

# Exact verified real models that exist in model/
REAL_ANIMAL_MODELS = {
    "Elephant": "elephant.glb",
    "Asiatic Lion": "lion.glb",
    "Lion": "lion.glb",
    "Water Buffalo": "Buffalo.glb",
    "Buffalo": "Buffalo.glb",
    "Red Ant": "redant.glb",
    "Ant": "ant.glb",
    "Alligator": "Alligator.glb",
    "Alpaca": "alpaca.glb",
    "Bear": "Bear.glb",
    "Bee": "Bee.glb",
    "Camel": "Camel.glb",
    "Cat": "Cat.glb",
    "Cow": "Cow.glb"
}

REAL_FRUIT_MODELS = {
    "Elaichi Banana": "banana.glb",
    "Banana": "banana.glb",
    "Blackberry": "blackberry.glb",
    "Blueberry": "blueberry.glb",
    "Apple": "Apple.glb",
    "Avocado": "Avocado.glb",
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

def match_model(name, mapping):
    clean_name = name.split(" (")[0].strip().lower()
    # 1. Exact match
    for k, v in mapping.items():
        if k.lower() == clean_name:
            return v
    # 2. Whole word boundary match, sorted by length descending
    sorted_keys = sorted(mapping.keys(), key=lambda x: len(x), reverse=True)
    for k in sorted_keys:
        pattern = r'\b' + re.escape(k.lower()) + r'\b'
        if re.search(pattern, clean_name):
            return mapping[k]
    return None

# Read current dataset_full.json
with open("c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/dataset_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for a in data.get("animals", []):
    name = a.get("name", "")
    matched = match_model(name, REAL_ANIMAL_MODELS)
    if matched:
        a["model"] = matched
        a["hasRealModel"] = True
    else:
        a["model"] = None
        a["hasRealModel"] = False

for fr in data.get("fruits", []):
    name = fr.get("name", "")
    matched = match_model(name, REAL_FRUIT_MODELS)
    if matched:
        fr["model"] = matched
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

print("Dataset updated successfully!")

