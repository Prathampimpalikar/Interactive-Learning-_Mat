import os
import shutil

base_dir = "c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat"
letter_model_dir = os.path.join(base_dir, "letter model")
letter_model_dir_nospace = os.path.join(base_dir, "letter_model")
model_dir = os.path.join(base_dir, "model")

os.makedirs(letter_model_dir_nospace, exist_ok=True)
os.makedirs(model_dir, exist_ok=True)

# Rename / copy 0 (1).glb to 0.glb in letter model
zero_src = os.path.join(letter_model_dir, "0 (1).glb")
zero_dest = os.path.join(letter_model_dir, "0.glb")
if os.path.exists(zero_src) and not os.path.exists(zero_dest):
    shutil.copy2(zero_src, zero_dest)
    print("Created 0.glb in letter model")

for item in os.listdir(letter_model_dir):
    src = os.path.join(letter_model_dir, item)
    if os.path.isfile(src):
        # copy to letter_model
        shutil.copy2(src, os.path.join(letter_model_dir_nospace, item))
        # copy to model/
        shutil.copy2(src, os.path.join(model_dir, item))

if os.path.exists(zero_src):
    shutil.copy2(zero_src, os.path.join(model_dir, "0.glb"))
    shutil.copy2(zero_src, os.path.join(letter_model_dir_nospace, "0.glb"))

print("Letter models copied to model/ and letter_model/")
