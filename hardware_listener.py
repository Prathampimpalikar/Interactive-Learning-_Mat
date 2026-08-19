import threading
import time

try:
    import serial
    import serial.tools.list_ports
    SERIAL_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    SERIAL_AVAILABLE = False


class HardwareListener:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HardwareListener, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.serial_port = None
        self.thread = None
        self.running = False
        self.active_window = None
        self.callback = None

        # Start scanning and reading in the background
        self.start()

    def register(self, window, callback):
        """Register the current active window and the function to handle hardware triggers."""
        self.active_window = window
        self.callback = callback
        print(f"[HardwareListener] Registered callback for window: {window}")

    def deregister(self):
        """Deregister when the window is destroyed."""
        self.active_window = None
        self.callback = None

    def start(self):
        if not SERIAL_AVAILABLE:
            print("[HardwareListener] 'pyserial' is not installed. Running in simulator/keyboard-only mode.")
            return
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_listener)
            self.thread.daemon = True
            self.thread.start()
            print("[HardwareListener] Background thread started.")

    def stop(self):
        self.running = False
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.close()
            except Exception:
                pass
        print("[HardwareListener] Stopped listener.")

    def _find_arduino_port(self):
        ports = serial.tools.list_ports.comports()
        # Look for typical Arduino descriptions or USB serial converters
        for port in ports:
            desc = port.description.lower()
            if any(term in desc for term in ["arduino", "ch340", "usb-serial", "usb serial", "ftdi"]):
                return port.device
        # Fallback to the first available COM port
        if ports:
            return ports[0].device
        return None

    def _run_listener(self):
        while self.running:
            port = self._find_arduino_port()
            if not port:
                # No Arduino/COM ports found, wait and scan again
                time.sleep(2)
                continue

            try:
                print(f"[HardwareListener] Connecting to COM port: {port}...")
                self.serial_port = serial.Serial(port, 9600, timeout=1)
                print(f"[HardwareListener] Successfully connected to {port}!")

                while self.running and self.serial_port.is_open:
                    if self.serial_port.in_waiting > 0:
                        try:
                            line = self.serial_port.readline().decode("utf-8", errors="ignore").strip()
                            if line:
                                print(f"[HardwareListener] Received: '{line}'")
                                # Dispatch callback to the Tkinter thread
                                if self.active_window and self.callback:
                                    try:
                                        if self.active_window.winfo_exists():
                                            self.active_window.after(0, self.callback, line)
                                    except Exception as e:
                                        print(f"[HardwareListener] Callback invocation error: {e}")
                        except Exception as e:
                            print(f"[HardwareListener] Serial read error: {e}")
                            break
                    else:
                        time.sleep(0.05)
            except Exception as e:
                print(f"[HardwareListener] Serial port connection error on {port}: {e}")
                time.sleep(2)  # Retry connection after a short wait


# Instantiate global listener
listener = HardwareListener()
