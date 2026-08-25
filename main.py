"""
AlphaMat — Smart Interactive 3D Learning Mat & EduTech Platform
Main Application Launcher & Server Bridge
"""

import os
import sys
import time
import webbrowser
from server import start_server

def main():
    # Ensure UTF-8 output on Windows consoles
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 70)
    print(">> AlphaMat - Smart Interactive 3D Learning Mat & EduTech Platform")
    print("=" * 70)
    print("\n[INFO] Starting local WebXR 3D server & assets bridge...")

    # Start local HTTP server serving root directory & GLB 3D models
    httpd, port = start_server()

    web_url = f"http://localhost:{port}"
    print(f"\n[SUCCESS] AlphaMat Web Platform is live at: {web_url}")

    # Start Hardware Serial Listener for USB-connected Arduino/ESP32
    try:
        from hardware_listener import listener
        from firebase import update_current_letter

        def on_serial_received(data):
            val = str(data).strip().upper()
            print(f"[Hardware Bridge] Received serial signal: '{val}'")
            for char in ["A", "B", "C", "D", "E", "F"]:
                if char in val:
                    print(f"[Hardware Bridge] >>> Updating Firebase with Letter: '{char}' <<<")
                    update_current_letter(char)
                    break

        listener.callback = on_serial_received
        listener.start()
        print("[SUCCESS] Hardware USB Listener active & bridged to Firebase/Web platform!")
    except Exception as e:
        print(f"[NOTE] Serial listener setup info: {e}")

    print("[INFO] Launching AlphaMat in your web browser...")

    # Open web platform automatically in default browser
    try:
        webbrowser.open(web_url)
    except Exception as e:
        print(f"[NOTE] Please open {web_url} in your browser: {e}")

    print("\n" + "-" * 70)
    print(f">> System Ready! Step on your physical mat or explore at: {web_url}")
    print("   • Press Ctrl+C in this terminal to stop the server.")
    print("-" * 70 + "\n")

    # Keep server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Stopping AlphaMat server. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()