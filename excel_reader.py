import pandas as pd

ANIMAL_FILE = "dataset/Animals_Dataset.xlsx"
FRUIT_FILE = "dataset/Fruits_Dataset.xlsx"


def load_animals():
    return pd.read_excel(ANIMAL_FILE)


def load_fruits():
    return pd.read_excel(FRUIT_FILE)


def get_animals_by_letter(letter):
    df = load_animals()
    return df[df["Alphabet"].astype(str).str.strip().str.upper() == str(letter).strip().upper()]


def get_fruits_by_letter(letter):
    df = load_fruits()
    return df[df["Alphabet"].astype(str).str.strip().str.upper() == str(letter).strip().upper()]