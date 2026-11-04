# ==============================================================================
# AlphaMat - 5-Piezo MicroPython Controller (Letters A, B, C, D, E)
# Dynamic baseline calibration to prevent Pin 33 (Letter B) false triggers
# ==============================================================================

from machine import ADC, Pin
import time

pads = [
    {"letter": "A", "pin": 32, "adc": ADC(Pin(32)), "baseline": 0},
    {"letter": "B", "pin": 33, "adc": ADC(Pin(33)), "baseline": 0},
    {"letter": "C", "pin": 36, "adc": ADC(Pin(36)), "baseline": 0},  # VP Pin
    {"letter": "D", "pin": 34, "adc": ADC(Pin(34)), "baseline": 0},
    {"letter": "E", "pin": 35, "adc": ADC(Pin(35)), "baseline": 0},
]

for p in pads:
    p["adc"].atten(ADC.ATTN_11DB)

print("========================================")
print("  AlphaMat 5-Piezo Controller Ready")
print("  Calibrating baselines...")

time.sleep_ms(300)
for p in pads:
    sum_val = sum(p["adc"].read() for _ in range(30))
    p["baseline"] = sum_val // 30
    print(f"  • Letter {p['letter']} (Pin {p['pin']}) Baseline: {p['baseline']}")

print("  Calibration complete! System ready.")
print("========================================")

SPIKE_THRESHOLD = 350

while True:
    for p in pads:
        val = p["adc"].read()
        spike = val - p["baseline"]
        if spike >= SPIKE_THRESHOLD:
            print("STEP DETECTED -> Letter:", p["letter"], f"(Pin {p['pin']}) | Spike:", spike)
            print(p["letter"])
            time.sleep_ms(400)
            break

    time.sleep_ms(10)
