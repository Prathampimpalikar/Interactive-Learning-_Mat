"""
AlphaMat - Hardware Serial Listener for ESP32 / Arduino Piezo Mat
Reads serial signals from physical sensors, auto-detects COM ports, and writes hardware_event.json.
"""

import os
import json
import time
import threading
import serial
import serial.tools.list_ports

# ==============================================================================
# CONFIGURATION & 3-IN-1 MAT MULTI-PIN MAPPING
# ==============================================================================
DEFAULT_PORT = "COM5"
BAUD_RATE = 115200

# Mapping GPIO and character triggers to primary letters:
# Block 1: GPIO 32 -> A (also responds to N, 0)
# Block 2: GPIO 33 -> B (also responds to O, 1)
# Block 3: GPIO 25 -> C (also responds to P, 2)
# Block 4: GPIO 26 -> D (also responds to Q, 3)
GPIO_TO_LETTER = {
    32: "A",
    33: "B",
    25: "C",
    26: "D",
    27: "E",
    14: "F",
    12: "G",
    13: "H",
    15: "I",
    2:  "J",
    4:  "K",
    16: "L",
    17: "M"
}

LETTER_TO_GPIO = {
    "A": 32, "N": 32, "0": 32,
    "B": 33, "O": 33, "1": 33,
    "C": 25, "P": 25, "2": 25,
    "D": 26, "Q": 26, "3": 26,
    "E": 27, "R": 27, "4": 27,
    "F": 14, "S": 14, "5": 14,
    "G": 12, "T": 12, "6": 12,
    "H": 13, "U": 13, "7": 13,
    "I": 15, "V": 15, "8": 15,
    "J": 2,  "W": 2,  "9": 2,
    "K": 4,  "X": 4,  "10": 4,
    "L": 16, "Y": 16,
    "M": 17, "Z": 17
}

EVENT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hardware_event.json")

BOOT_KEYWORDS = [
    "rst:", "boot:", "configsip", "load:", "entry", "ets", "waiting",
    "ready", "esp32 ready", "clk", "cs", "mode:", "flash:", "cpu"
]


def find_available_port():
    """Auto-detect connected Arduino / ESP32 COM port."""
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        return None
    for p in ports:
        desc = p.description.lower()
        if "ch340" in desc or "cp210" in desc or "usb" in desc or "serial" in desc or "arduino" in desc or "esp" in desc:
            return p.device
    return ports[0].device


def write_hardware_event(letter, gpio=32):
    """Write hardware event JSON file for the website to read."""
    event_data = {
        "letter": letter,
        "gpio": gpio,
        "timestamp": time.time()
    }
    temp_file = f"{EVENT_FILE}.tmp"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(event_data, f, indent=4)
        if os.path.exists(temp_file):
            os.replace(temp_file, EVENT_FILE)
    except Exception:
        try:
            with open(EVENT_FILE, "w", encoding="utf-8") as f:
                json.dump(event_data, f, indent=4)
        except Exception as e:
            print(f"[Error writing hardware_event.json]: {e}")


def is_boot_message(line):
    lower_line = line.lower()
    for kw in BOOT_KEYWORDS:
        if kw in lower_line:
            return True
    return False


def run_hardware_listener(callback=None):
    """Main listener loop connecting to ESP32 / Arduino."""
    port_to_use = DEFAULT_PORT
    detected_port = find_available_port()
    if detected_port:
        port_to_use = detected_port

    print("=" * 60)
    print(f"📡 AlphaMat Hardware Serial Listener starting on port '{port_to_use}'...")
    print("=" * 60)

    esp32 = None
    try:
        esp32 = serial.Serial(port_to_use, BAUD_RATE, timeout=1)
        print(f"[SUCCESS] ESP32 / Arduino CONNECTED on {port_to_use}")
        print("Waiting for piezoelectric sensor step triggers...\n")

        time.sleep(1.5)
        try:
            esp32.reset_input_buffer()
        except Exception:
            pass

        while True:
            if esp32.in_waiting > 0:
                raw = esp32.readline()
                try:
                    line = raw.decode("utf-8", errors="ignore").strip()
                except Exception:
                    continue

                if not line or is_boot_message(line):
                    continue

                clean_text = line.upper()

                # Check if raw text is numeric GPIO (e.g. 32)
                resolved_letter = None
                gpio_num = 32

                if clean_text.isdigit():
                    num = int(clean_text)
                    if num in GPIO_TO_LETTER:
                        resolved_letter = GPIO_TO_LETTER[num]
                        gpio_num = num
                elif "32" in clean_text or "GPIO 32" in clean_text:
                    resolved_letter = "A"
                    gpio_num = 32
                elif clean_text in LETTER_TO_GPIO:
                    gpio_num = LETTER_TO_GPIO[clean_text]
                    # Map secondary chars (like N -> A, O -> B) or keep exact letter
                    resolved_letter = clean_text if clean_text.isalpha() else GPIO_TO_LETTER.get(gpio_num, "A")
                elif len(clean_text) == 1 and clean_text.isalpha():
                    resolved_letter = clean_text
                    gpio_num = LETTER_TO_GPIO.get(clean_text, 32)

                if resolved_letter:
                    print(f"⚡ [ESP32 Piezo Step Detected]: '{clean_text}' -> Letter {resolved_letter} (GPIO {gpio_num})")
                    write_hardware_event(resolved_letter, gpio_num)

                    if callback:
                        try:
                            callback(resolved_letter)
                        except Exception:
                            pass

            time.sleep(0.05)

    except serial.SerialException as e:
        err_msg = str(e)
        if "PermissionError" in err_msg or "Access is denied" in err_msg or "13" in err_msg:
            print("=" * 60)
            print(f"Could not connect to sensor: {port_to_use} IS BUSY")
            print("=" * 60)
            print("Possible causes:")
            print("  - Arduino Serial Monitor is open (Please close it)")
            print("  - Thonny IDE is open")
        else:
            print("=" * 60)
            print(f"Could not connect to ESP32 on port '{port_to_use}'")
            print("ESP32 / Arduino NOT CONNECTED (Using Virtual Sensor Simulator)")
            print("Available detected ports:", [p.device for p in serial.tools.list_ports.comports()])
            print("=" * 60)

    except KeyboardInterrupt:
        print("\nHardware listener stopped.")

    finally:
        if esp32 and esp32.is_open:
            try:
                esp32.close()
            except Exception:
                pass


class HardwareListenerThread:
    def __init__(self):
        self.callback = None
        self._thread = None

    def start(self):
        self._thread = threading.Thread(target=run_hardware_listener, args=(self.callback,), daemon=True)
        self._thread.start()


listener = HardwareListenerThread()

if __name__ == "__main__":
    run_hardware_listener()