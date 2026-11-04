"""
AlphaMat - Multi-Piezo Serial Listener (Letters A to E: GPIO 32, 33, 36/VP, 34, 35)
Listens for physical taps on ESP32 GPIOs and triggers Alphabets in the web app.
"""

import os
import json
import time
import threading
import serial
import serial.tools.list_ports

# ==============================================================================
# CONFIGURATION: 5-PIEZO MODE (A: 32, B: 33, C: 36/VP, D: 34, E: 35)
# ==============================================================================
DEFAULT_PORT = "COM5"
BAUD_RATE = 115200

EVENT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hardware_event.json")

BOOT_KEYWORDS = [
    "rst:", "boot:", "configsip", "load:", "entry", "ets", "waiting",
    "ready", "esp32 ready", "alphamat_sensor_ready", "alphamat_piezo_a_ready",
    "alphamat_dual_piezo_ready", "alphamat_multi_piezo_ready", "alphamat_5_piezo_ready", "baseline",
    "clk", "cs", "mode:", "flash:", "cpu", "chip", "rom:", "baud", "compiled",
    "connecting", "wifi", "ip address"
]


def find_available_port():
    """Auto-detect connected ESP32 / Arduino COM port."""
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        return None
    for p in ports:
        desc = p.description.lower()
        if "ch340" in desc or "cp210" in desc or "usb" in desc or "serial" in desc or "arduino" in desc or "esp" in desc:
            return p.device
    return ports[0].device if ports else None


_clear_timer = None

def write_hardware_event(letter="A", gpio=34, auto_clear=True):
    """Write hardware event JSON file for the website to read."""
    global _clear_timer
    if _clear_timer is not None:
        try:
            _clear_timer.cancel()
        except Exception:
            pass
        _clear_timer = None

    event_data = {
        "letter": letter,
        "gpio": gpio,
        "timestamp": time.time()
    }
    temp_file = f"{EVENT_FILE}.tmp"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(event_data, f)
        if os.path.exists(temp_file):
            os.replace(temp_file, EVENT_FILE)
    except Exception:
        try:
            with open(EVENT_FILE, "w", encoding="utf-8") as f:
                json.dump(event_data, f)
        except Exception as e:
            print(f"[Error writing hardware_event.json]: {e}")

    # Auto-clear event after 3.0s (timestamp comparison prevents duplicate reads)
    if letter and auto_clear:
        def _do_clear():
            write_hardware_event("", 0, auto_clear=False)
        _clear_timer = threading.Timer(3.0, _do_clear)
        _clear_timer.daemon = True
        _clear_timer.start()


def is_boot_message(line):
    lower_line = line.lower().strip()
    if not lower_line:
        return True
    for kw in BOOT_KEYWORDS:
        if kw in lower_line:
            return True
    return False


def parse_serial_message(line):
    """
    Parser for 5-Piezo Hardware Sensors (Letters A through E):
    - Piezo A (GPIO 32 -> Letter 'A')
    - Piezo B (GPIO 33 -> Letter 'B')
    - Piezo C (GPIO 36 / VP -> Letter 'C')
    - Piezo D (GPIO 34 -> Letter 'D')
    - Piezo E (GPIO 35 -> Letter 'E')
    """
    clean_text = line.strip().upper()
    if not clean_text or is_boot_message(clean_text):
        return None, None

    # Allowed active letters: A, B, C, D, E
    letter_gpio_map = {
        "A": 32,
        "B": 33,
        "C": 36,
        "D": 34,
        "E": 35
    }

    # Strict check: direct letter match
    if clean_text in letter_gpio_map:
        return clean_text, letter_gpio_map[clean_text]

    # Exact matches for Letter A (Pin 32 / GPIO 32)
    if clean_text in ["A", "32", "GPIO 32", "GPIO32", "PIN 32", "STEP:A", "STEP标志", "STEP A", "LETTER A", "LETTER: A", "TAP A"]:
        return "A", 32

    # Exact matches for Letter B (Pin 33 / GPIO 33)
    if clean_text in ["B", "33", "GPIO 33", "GPIO33", "PIN 33", "STEP:B", "STEP B", "LETTER B", "LETTER: B", "TAP B"]:
        return "B", 33

    # Exact matches for Letter C (Pin VP / GPIO 36)
    if clean_text in ["C", "36", "VP", "SENSOR_VP", "PIN VP", "GPIO 36", "GPIO36", "PIN 36", "STEP:C", "STEP C", "LETTER C", "LETTER: C", "TAP C"]:
        return "C", 36

    # Exact matches for Letter D (Pin 34 / GPIO 34)
    if clean_text in ["D", "34", "GPIO 34", "GPIO34", "PIN 34", "STEP:D", "STEP D", "LETTER D", "LETTER: D", "TAP D"]:
        return "D", 34

    # Exact matches for Letter E (Pin 35 / GPIO 35)
    if clean_text in ["E", "35", "GPIO 35", "GPIO35", "PIN 35", "STEP:E", "STEP E", "LETTER E", "LETTER: E", "TAP E"]:
        return "E", 35

    # Precise prefixed checks
    if clean_text.startswith("LETTER: A") or clean_text.startswith("STEP: A") or clean_text == "TAP A":
        return "A", 32
    if clean_text.startswith("LETTER: B") or clean_text.startswith("STEP: B") or clean_text == "TAP B":
        return "B", 33
    if clean_text.startswith("LETTER: C") or clean_text.startswith("STEP: C") or clean_text == "TAP C":
        return "C", 36
    if clean_text.startswith("LETTER: D") or clean_text.startswith("STEP: D") or clean_text == "TAP D":
        return "D", 34
    if clean_text.startswith("LETTER: E") or clean_text.startswith("STEP: E") or clean_text == "TAP E":
        return "E", 35

    return None, None


def run_hardware_listener(callback=None):
    """Main listener loop for Multi-Piezo Hardware Controller."""
    print("=" * 65)
    print("📡 AlphaMat Hardware Listener Active (Letters A, B, C, D, E)")
    print("   • Letter 'A': Pin 32 (GPIO 32)")
    print("   • Letter 'B': Pin 33 (GPIO 33)")
    print("   • Letter 'C': Pin VP (GPIO 36 / SENSOR_VP)")
    print("   • Letter 'D': Pin 34 (GPIO 34)")
    print("   • Letter 'E': Pin 35 (GPIO 35)")
    print("   • Mode: PRESS ONLY (Automatic Selection OFF)")
    print("=" * 65)

    # Clear old event file on start so browser doesn't auto-switch on refresh
    write_hardware_event("", 0)

    last_trigger_time = 0
    TRIGGER_COOLDOWN = 0.01  # Ultra-fast 0.01s (10ms) cooldown for maximum data receiving frequency

    while True:
        port_to_use = find_available_port() or DEFAULT_PORT
        esp32 = None

        try:
            esp32 = serial.Serial(port_to_use, BAUD_RATE, timeout=1)
            print(f"[SUCCESS] ESP32 / ARDUINO CONNECTED on {port_to_use}")
            print(">> Waiting for physical tap on Piezo Pads (A:32, B:33, C:36/VP, D:34, E:35)...\n")

            # Allow board to finish setup/calibration and flush boot buffer
            time.sleep(2.0)
            try:
                esp32.reset_input_buffer()
                esp32.reset_output_buffer()
            except Exception:
                pass

            last_activity_time = time.time()

            while True:
                now = time.time()

                if esp32.in_waiting > 0:
                    try:
                        raw = esp32.readline()
                        line = raw.decode("utf-8", errors="ignore").strip()
                    except Exception:
                        continue

                    if not line:
                        continue

                    resolved_letter, gpio_num = parse_serial_message(line)

                    if resolved_letter:
                        if (now - last_trigger_time) >= TRIGGER_COOLDOWN:
                            last_trigger_time = now
                            print(f"[PIEZO] GPIO {gpio_num} detected")
                            print(f"[HARDWARE] Letter {resolved_letter}\n")

                            write_hardware_event(resolved_letter, gpio_num)

                            if callback:
                                try:
                                    callback(resolved_letter)
                                except Exception:
                                    pass

                time.sleep(0.001)

        except serial.SerialException as e:
            err_msg = str(e)
            if "PermissionError" in err_msg or "Access is denied" in err_msg or "13" in err_msg:
                print(f"[NOTE] Port {port_to_use} is currently busy. Retrying in 2s...")
            else:
                print(f"[SEARCHING] ESP32 not detected on {port_to_use}. Retrying in 2s...")
            time.sleep(2.0)

        except KeyboardInterrupt:
            print("\nHardware listener stopped.")
            break

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