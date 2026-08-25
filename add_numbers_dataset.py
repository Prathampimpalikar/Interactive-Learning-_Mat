import json
import os

# Complete Numbers 0 to 10 Dataset
numbers_data = [
    {
        "id": "number_0",
        "type": "number",
        "alphabet": "0",
        "number": "0",
        "name": "Number 0 — Zero (Shunya / Invention of Zero)",
        "scientificName": "Discovery of Zero by Aryabhata & Brahmagupta (Ancient India)",
        "category": "Mathematics & History",
        "color": "Cosmic Gold & Celestial Blue",
        "superpower": "Universal Base of Mathematics, Binary Code & Space Exploration",
        "inventor": "Aryabhata (476–550 CE) & Brahmagupta (598–668 CE)",
        "origin": "Ancient India (Mathematical treatise 'Aryabhatiya' & 'Brahmasphutasiddhanta')",
        "funFact": "Zero is the only number that is neither positive nor negative, and multiplying any number by 0 gives 0!",
        "description": "Who invented Zero? The concept of Zero (called 'Shunya' in Sanskrit, meaning void or sky) and the place-value decimal system were pioneered by ancient Indian mathematician-astronomer Aryabhata in the 5th century CE. In 628 CE, the great Indian astronomer Brahmagupta formulated the world's first mathematical rules and algebraic operations for Zero in his masterwork 'Brahmasphutasiddhanta'. This revolutionary Indian discovery traveled across the Arab world to Europe, giving humanity modern arithmetic, algebra, computers, and rocket navigation!",
        "image": "aryabhata.jpg",
        "model": "0.glb",
        "hasRealModel": True,
        "hasRealImage": True
    },
    {
        "id": "number_1",
        "type": "number",
        "alphabet": "1",
        "number": "1",
        "name": "Number 1 — One (Ek)",
        "scientificName": "First Positive Integer & Multiplicative Identity",
        "category": "Mathematics",
        "color": "Ruby Red & Golden Yellow",
        "superpower": "Multiplicative Identity (Any number × 1 = itself)",
        "funFact": "1 is the first odd number and the fundamental building block of all counting numbers!",
        "description": "Number 1 represents unity, origins, and the start of all numbers. In arithmetic, multiplying any number by 1 leaves it unchanged, making 1 the unique multiplicative identity element across all mathematics.",
        "image": "logo.jpg",
        "model": "1.glb",
        "hasRealModel": True,
        "hasRealImage": True
    },
    {
        "id": "number_2",
        "type": "number",
        "alphabet": "2",
        "number": "2",
        "name": "Number 2 — Two (Do)",
        "scientificName": "First Even Number & Only Even Prime Number",
        "category": "Mathematics",
        "color": "Ocean Blue & Turquoise",
        "superpower": "Foundation of Binary Code (0 and 1) running all digital technology",
        "funFact": "2 is the only number in the entire universe that is both an even number and a prime number!",
        "description": "Number 2 is the base of the binary numeral system (Base-2) that powers every smartphone, computer chip, and internet server on planet Earth. It represents pairs, symmetry, and duality in nature.",
        "image": "logo.jpg",
        "model": "2.glb",
        "hasRealModel": True,
        "hasRealImage": True
    },
    {
        "id": "number_3",
        "type": "number",
        "alphabet": "3",
        "number": "3",
        "name": "Number 3 — Three (Teen)",
        "scientificName": "Strongest Geometry: Triangle (3-Sided Polygon)",
        "category": "Mathematics",
        "color": "Emerald Green & Lime",
        "superpower": "Rigid Geometric Stability (Triangles never deform)",
        "funFact": "Triangles with 3 sides are the strongest structural shapes used to build towering bridges and skyscrapers!",
        "description": "Number 3 forms the triangle, the only polygon that is inherently rigid and cannot be deformed without breaking its edges. It is fundamental in trigonometry, 3D space (X, Y, Z axes), and physics.",
        "image": "logo.jpg",
        "model": "3.glb",
        "hasRealModel": True,
        "hasRealImage": True
    },
    {
        "id": "number_4",
        "type": "number",
        "alphabet": "4",
        "number": "4",
        "name": "Number 4 — Four (Char)",
        "scientificName": "Cardinal Directions & Square Geometry",
        "category": "Mathematics",
        "color": "Vibrant Orange & Amber",
        "superpower": "First Composite Number & 4 Cardinal Directions (N, S, E, W)",
        "funFact": "A square has 4 equal sides and 4 interior right angles of 90 degrees that add up to 360 degrees!",
        "description": "Number 4 defines navigation through the four cardinal directions (North, South, East, West), the four seasons of nature (Spring, Summer, Autumn, Winter), and the perfect symmetry of a square.",
        "image": "logo.jpg",
        "model": "4.glb",
        "hasRealModel": True,
        "hasRealImage": True
    },
    {
        "id": "number_5",
        "type": "number",
        "alphabet": "5",
        "number": "5",
        "name": "Number 5 — Five (Paanch)",
        "scientificName": "Pentagonal Symmetry & 5 Human Senses",
        "category": "Mathematics",
        "color": "Royal Purple & Magenta",
        "superpower": "Pentagonal Golden Ratio & 5 Digits per Human Hand",
        "funFact": "Starfish, apple blossoms, and morning glory flowers all display natural 5-fold radial symmetry!",
        "description": "Number 5 is closely tied to human biology with 5 fingers on each hand, 5 toes on each foot, and the 5 senses (Sight, Hearing, Taste, Smell, Touch). It is also the basis of the pentagon and the golden ratio spiral.",
        "image": "logo.jpg",
        "model": "5.glb",
        "hasRealModel": True,
        "hasRealImage": True
    },
    {
        "id": "number_6",
        "type": "number",
        "alphabet": "6",
        "number": "6",
        "name": "Number 6 — Six (Chhah)",
        "scientificName": "First Perfect Number (1 + 2 + 3 = 6) & Hexagonal Hive",
        "category": "Mathematics",
        "color": "Golden Honey & Amber",
        "superpower": "Hexagonal Tiling (Highest structural efficiency in nature)",
        "funFact": "Honeybees build their hives with 6-sided hexagons because it uses the least wax and holds the most honey!",
        "description": "Number 6 is the smallest 'perfect number' because the sum of its proper divisors equals itself (1 + 2 + 3 = 6). In nature, snowflakes and bee honeycombs always form 6-sided hexagonal geometry.",
        "image": "logo.jpg",
        "model": "6.glb",
        "hasRealModel": True,
        "hasRealImage": True
    },
    {
        "id": "number_7",
        "type": "number",
        "alphabet": "7",
        "number": "7",
        "name": "Number 7 — Seven (Saat)",
        "scientificName": "VIBGYOR Rainbow Spectrum & Weekly Cycle",
        "category": "Mathematics",
        "color": "Rainbow Spectrum (VIBGYOR)",
        "superpower": "Optical Dispersion of Light into 7 Distinct Spectral Colors",
        "funFact": "Sunlight passing through raindrops splits into exactly 7 spectral colors: Violet, Indigo, Blue, Green, Yellow, Orange, and Red!",
        "description": "Number 7 is celebrated across science and cultures: the 7 colors of the rainbow, the 7 days of the week, the 7 continents on Earth, and the 7 notes of the musical octave (Sa Re Ga Ma Pa Dha Ni).",
        "image": "logo.jpg",
        "model": "7.glb",
        "hasRealModel": True,
        "hasRealImage": True
    },
    {
        "id": "number_8",
        "type": "number",
        "alphabet": "8",
        "number": "8",
        "name": "Number 8 — Eight (Aath)",
        "scientificName": "Octagonal Symmetry & Infinity Symbol (∞)",
        "category": "Mathematics",
        "color": "Cobalt Blue & Cyan",
        "superpower": "Sideways 8 forms the universal Infinity Symbol (∞)",
        "funFact": "When turned on its side, the number 8 becomes the mathematical lemniscate symbol for infinity (∞)!",
        "description": "Number 8 is the basis of an octagon (8 sides, like a stop sign), the 8 legs of an octopus and spider, and in computer science, 8 bits make up 1 byte of digital information.",
        "image": "logo.jpg",
        "model": "8.glb",
        "hasRealModel": True,
        "hasRealImage": True
    },
    {
        "id": "number_9",
        "type": "number",
        "alphabet": "9",
        "number": "9",
        "name": "Number 9 — Nine (Nau)",
        "scientificName": "Highest Single-Digit Decimal & Digital Root Magic",
        "category": "Mathematics",
        "color": "Fiery Crimson & Sunset Coral",
        "superpower": "Magical Digital Root (Multiples of 9 always sum to 9)",
        "funFact": "In the 9 times table, adding the digits of any answer always equals 9 (e.g. 9 × 7 = 63 -> 6 + 3 = 9)!",
        "description": "Number 9 is the highest single-digit number in the decimal system. It holds unique mathematical properties: the sum of the digits of any multiple of 9 is always a multiple of 9.",
        "image": "logo.jpg",
        "model": "9.glb",
        "hasRealModel": True,
        "hasRealImage": True
    },
    {
        "id": "number_10",
        "type": "number",
        "alphabet": "10",
        "number": "10",
        "name": "Number 10 — Ten (Das)",
        "scientificName": "Base of the Universal Decimal Place-Value System",
        "category": "Mathematics",
        "color": "Gleaming Gold & Diamond White",
        "superpower": "Foundation of the Global Metric System & Decimal Counting",
        "funFact": "Humans count in Base-10 (Decimal) worldwide because our ancient ancestors used their 10 fingers!",
        "description": "Number 10 is the foundation of the decimal numeral system and the metric system (meters, kilograms, liters). Combining 1 and 0, it represents completion and the transition to two-digit numbers.",
        "image": "logo.jpg",
        "model": "10.glb",
        "hasRealModel": True,
        "hasRealImage": True
    }
]

# Read existing animals and fruits from build_full_dataset
with open("c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/dataset_full.json", "r", encoding="utf-8") as f:
    existing = json.load(f)

existing["numbers"] = numbers_data

# Write dataset_full.json
with open("c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/dataset_full.json", "w", encoding="utf-8") as f:
    json.dump(existing, f, indent=2)

# Write js/data.js
js_content = "const ALPHAMAT_DATA = " + json.dumps(existing, indent=2) + ";\n"
with open("c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/js/data.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print("Added 0-10 numbers dataset with Aryabhata invention of zero to js/data.js & dataset_full.json!")
