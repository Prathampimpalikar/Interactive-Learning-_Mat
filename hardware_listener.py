"""
AlphaMat - Hardware Serial Listener for ESP32 Piezo Mat
Reads serial signals from ESP32, creates hardware_event.json for web platform.
"""

import os
import json
import time
import threading
import serial

# ==========================================
# CONFIGURATION
# ==========================================
PORT = "COM5"
BAUD_RATE = 115200

# Future 26-sensor mapping architecture
# Current test: GPIO 32 -> Letter A
GPIO_TO_LETTER = {
    32: "A"
}
LETTER_TO_GPIO = {v: k for k, v in GPIO_TO_LETTER.items()}

# Event output file in project root
EVENT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hardware_event.json")

# ESP32 boot messages to ignore
BOOT_KEYWORDS = [
    "rst:", "boot:", "configsip", "load:", "entry", "ets", "waiting",
    "ready", "esp32 ready", "clk", "cs", "mode:", "flash:", "cpu"
]


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
        # Fallback direct write
        try:
            with open(EVENT_FILE, "w", encoding="utf-8") as f:
                json.dump(event_data, f, indent=4)
        except Exception as e:
            print(f"[Error writing hardware_event.json]: {e}")


def is_boot_message(line):
    """Check if the incoming line is an ESP32 boot/debug message."""
    lower_line = line.lower()
    for kw in BOOT_KEYWORDS:
        if kw in lower_line:
            return True
    return False


def run_hardware_listener(callback=None):
    """Main listener loop connecting to ESP32."""
    esp32 = None
    try:
        esp32 = serial.Serial(PORT, BAUD_RATE, timeout=1)

        print("ESP32 CONNECTED")
        print("Waiting for piezo...\n")

        # Allow serial port to stabilize
        time.sleep(1.5)

        # Clear any stale startup buffer
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

                if not line:
                    continue

                # Filter out boot log lines
                if is_boot_message(line):
                    continue

                letter = line.upper()

                # Process valid single letter
                if letter in GPIO_TO_LETTER.values() or len(letter) == 1 and letter.isalpha():
                    gpio_pin = LETTER_TO_GPIO.get(letter, 32)

                    print(f"ESP32: {letter}")
                    print("PIEZO PRESSED")
                    print(f"LETTER {letter} DETECTED\n")

                    write_hardware_event(letter, gpio_pin)

                    if callback:
                        try:
                            callback(letter)
                        except Exception:
                            pass

            time.sleep(0.05)

    except serial.SerialException as e:
        err_msg = str(e)
        if "PermissionError" in err_msg or "Access is denied" in err_msg or "13" in err_msg:
            print("=" * 60)
            print(f"Could not connect to ESP32: {PORT} IS BUSY")
            print("=" * 60)
            print(f"COM5 IS BUSY")
            print("Possible causes:")
            print("  - Arduino Serial Monitor is open (Please CLOSE it)")
            print("  - Thonny is open")
            print("  - Another serial application or listener is open")
            print("=" * 60)
        else:
            print("=" * 60)
            print(f"Could not connect to ESP32 on port '{PORT}'")
            print("=" * 60)
            print("ESP32 NOT CONNECTED")
            print("Check USB cable and COM port.")
            print(f"Details: {e}")
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
    """Threaded wrapper for main.py integration."""
    def __init__(self):
        self.callback = None
        self._thread = None

    def start(self):
        self._thread = threading.Thread(target=run_hardware_listener, args=(self.callback,), daemon=True)
        self._thread.start()


# Global listener instance for main.py integration
listener = HardwareListenerThread()


if __name__ == "__main__":
    run_hardware_listener()