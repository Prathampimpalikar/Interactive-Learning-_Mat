import os
import shutil
import json

model_dir = "c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/model"

# Check all files in model_dir and make clean aliases if needed
files = os.listdir(model_dir)
print("Files in model dir:", files)

# Alias map
aliases = {
    "Asiatic Lion .glb": ["Asiatic Lion.glb", "lion.glb", "Lion.glb"],
    "Banana .glb": ["Banana.glb", "banana.glb"],
    "Blackberries.glb": ["blackberry.glb", "Blackberry.glb"],
    "Blueberries.glb": ["blueberry.glb", "Blueberry.glb"],
    "Red ant.glb": ["redant.glb", "Red Ant.glb", "ant.glb"],
    "Alligator.glb": ["alligator.glb"],
    "Apple.glb": ["apple.glb"],
    "Avocado.glb": ["avocado.glb"],
    "Bear.glb": ["bear.glb"],
    "Bee.glb": ["bee.glb"],
    "Buffalo.glb": ["buffalo.glb"],
    "Camel.glb": ["camel.glb"],
    "Cat.glb": ["cat.glb"],
    "Cherry.glb": ["cherry.glb"],
    "Coconut.glb": ["coconut.glb"],
    "Cow.glb": ["cow.glb"],
    "Asiatic Elephant.glb": ["elephant.glb", "Elephant.glb"],
    "alpaca.glb": ["Alpaca.glb"]
}

for src_name, target_list in aliases.items():
    src_path = os.path.join(model_dir, src_name)
    if os.path.exists(src_path):
        for tgt in target_list:
            tgt_path = os.path.join(model_dir, tgt)
            if not os.path.exists(tgt_path):
                shutil.copy2(src_path, tgt_path)
                print(f"Created alias: {tgt} from {src_name}")

print("Updated models in directory:", os.listdir(model_dir))
