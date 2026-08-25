# 🚀 AlphaMat — Software Requirements, Libraries & Execution Guide

This document provides the complete list of **software, tools, libraries, dependencies**, and **step-by-step instructions** required to run, develop, and deploy the **Interactive Learning Mat (AlphaMat)** platform.

---

## 📋 1. Software & System Requirements

Before running the application, ensure the following core software is installed on your computer:

| Software | Required Version | Purpose | Download / Installation Link |
| :--- | :--- | :--- | :--- |
| **Python** | `3.9` to `3.12` | Main backend runtime, serial listener, HTTP server, and GUI apps | [python.org/downloads](https://www.python.org/downloads/) *(Ensure **"Add Python to PATH"** is checked during install)* |
| **Web Browser** | Latest Chrome, Edge, Firefox, Brave, or Safari | Renders 3D models, WebXR Augmented Reality, sound synthesis, and interactive UI | Pre-installed / [google.com/chrome](https://www.google.com/chrome/) |
| **Git** *(Optional)* | `2.x+` | Version control and cloning the repository | [git-scm.com](https://git-scm.com/) |
| **Arduino IDE** *(Optional - For Hardware)* | `v2.x` or `v1.8.x` | Compiling and uploading `.ino` sketch to Arduino Uno/Nano or ESP32 | [arduino.cc/en/software](https://www.arduino.cc/en/software) |
| **Thonny IDE** *(Optional - For MicroPython)* | `v4.x+` | Uploading `boot.py` and `piezo_controller.py` to MicroPython boards | [thonny.org](https://thonny.org/) |
| **USB-to-UART Drivers** *(For Hardware)* | CH340 or CP210x | Allows Windows to detect USB connected ESP32 / Arduino boards (COM Port) | [Silicon Labs CP210x](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers) / CH340 Driver |

---

## 📦 2. Required Libraries & Dependencies

All Python dependencies are defined in [`requirements.txt`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/requirements.txt).

### A. Python Packages

| Package Name | Purpose in Project |
| :--- | :--- |
| `customtkinter` | Modern UI toolkit for desktop windows, buttons, cards, and animations |
| `pillow` (`PIL`) | Image loading, resizing, and rendering in desktop interfaces |
| `pandas` | Reading and parsing the educational dataset (`.xlsx` / `.json`) |
| `openpyxl` | Excel engine dependency required by Pandas to read Excel datasets |
| `firebase-admin` | Realtime Database cloud synchronization between physical mat & web app |
| `pyserial` | Listens to USB COM port signals from Arduino / ESP32 piezoelectric sensors |
| `requests` | Sends and receives HTTP REST requests to/from Firebase and cloud endpoints |
| `pyinstaller` *(Optional)* | Bundles the project into a standalone `.exe` installer |

### B. Frontend / Web CDN Libraries (Included in HTML)

The web platform runs directly in the browser and automatically loads these lightweight libraries:
- **Google `<model-viewer>` (`v3.4.0`)**: 3D model rendering, 360° rotation, and WebXR Augmented Reality (AR).
- **Lucide Icons**: Modern SVG icon set for UI buttons and cards.
- **Canvas-Confetti**: Celebration confetti animations when quizzes are completed.
- **Google Fonts (Outfit & Plus Jakarta Sans)**: High-resolution modern typography.

---

## 🎯 3. Which Python File is Required to Run?

### 🌟 Primary Main Entry Point:
To launch the complete integrated system (Web platform + 3D Viewer + Hardware Serial Listener + Local Server):
👉 **`main.py`**

```powershell
python main.py
```

### 🗂️ Overview of All Python (`.py`) Files in this Project:

| Python File | Role & Function | How to Run |
| :--- | :--- | :--- |
| [`main.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/main.py) | **Primary Launcher**: Starts the asset server, launches serial listener for hardware, and opens browser automatically. | `python main.py` |
| [`server.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/server.py) | Standalone local HTTP server for 3D GLB models and web files. | `python server.py` |
| [`hardware_listener.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/hardware_listener.py) | Connects to USB COM port (`COM5` by default) to read piezo footstep triggers. | `python hardware_listener.py` |
| [`login.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/login.py) | Desktop CustomTkinter login interface. | `python login.py` |
| [`splash.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/splash.py) | Desktop splash screen loader. | `python splash.py` |
| [`category.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/category.py) | Desktop category selection window (Animals / Fruits). | `python category.py` |
| [`selection.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/selection.py) | Desktop letter & object picker interface. | `python selection.py` |
| [`viewer.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/viewer.py) | Desktop 3D model & educational dossier launcher. | `python viewer.py` |
| [`firebase.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/firebase.py) / [`firebase_config.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/firebase_config.py) | Helper modules for Firebase Realtime Database updates. | Imported by other modules |
| [`excel_reader.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/excel_reader.py) | Helper module to filter dataset entries by letter and category. | Imported by other modules |
| [`piezo_controller.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/piezo_controller.py) | MicroPython script to flash onto ESP32 / NodeMCU hardware for WiFi-based direct Firebase push. | Flash via Thonny IDE |
| [`boot.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/boot.py) | MicroPython WiFi connection script for ESP32 / ESP8266. | Flash via Thonny IDE |

---

## 🛠️ 4. Step-by-Step Guide: How to Run the Software

### Method 1: One-Click Quick Launch (Windows)
Double-click the [`run.bat`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/run.bat) file located in the project folder. It will:
1. Detect Python automatically.
2. Create and activate a virtual environment (`venv`).
3. Install/upgrade all required packages from `requirements.txt`.
4. Launch `python main.py` and open your default browser.

---

### Method 2: Manual Terminal Execution (Recommended for Developers)

#### Step 1: Open Terminal / PowerShell
Open PowerShell or Command Prompt and navigate to the project directory:
```powershell
cd c:\Users\pimpa\Downloads\InteractiveLearningMat\InteractiveLearningMat
```

#### Step 2: Create and Activate a Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# (Or on Windows Command Prompt)
venv\Scripts\activate.bat
```

#### Step 3: Install Required Libraries
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Run the Application
```powershell
python main.py
```
> Your browser will open automatically at `http://localhost:8000` (or `http://localhost:8080`).

---

## 🔌 5. Hardware Setup (Optional Physical Mat Connection)

If you are connecting physical Piezoelectric sensors on Arduino / ESP32:

1. **Check COM Port**:
   - Open Windows **Device Manager** -> **Ports (COM & LPT)**.
   - Note the COM port number (e.g. `COM3`, `COM5`).
2. **Update Port in Code**:
   - Open [`hardware_listener.py`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/hardware_listener.py) line 15:
     ```python
     PORT = "COM5"  # Change to your actual COM port
     ```
3. **Upload Firmware**:
   - **For Arduino Uno / Nano**: Open [`arduino_code/arduino_uno_nano/arduino_uno_nano.ino`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/arduino_code/arduino_uno_nano/arduino_uno_nano.ino) in Arduino IDE, select your board and port, then click **Upload**.
   - **For ESP32 (MicroPython)**: Use Thonny IDE to upload `boot.py` and `piezo_controller.py`.

---

## 🌐 6. How to Deploy the Software

### Option A: Deploy the Web Platform to the Cloud (Free)
1. **GitHub Pages (Already Active)**:
   - Push the repository to GitHub.
   - Go to **Settings > Pages > Source** and select `main` branch root (`/`).
   - Live URL: `https://prathampimpalikar.github.io/Interactive-Learning-_Mat/`

2. **Netlify**:
   - Drop the project directory into [app.netlify.com/drop](https://app.netlify.com/drop) or connect your GitHub repository. The included [`netlify.toml`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/netlify.toml) configures headers and routing automatically.

3. **Vercel / Firebase Hosting**:
   - Run `firebase deploy` using the included [`FIREBASE.JSON`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/FIREBASE.JSON).

### Option B: Build a Standalone Windows Executable (`.exe`)
Run [`build.bat`](file:///c:/Users/pimpa/Downloads/InteractiveLearningMat/InteractiveLearningMat/build.bat) or run:
```powershell
pyinstaller InteractiveLearningMat.spec
```
The compiled `.exe` will be located inside the `dist/` folder.

---

## ❓ 7. Troubleshooting & FAQs

- **Issue**: `python: command not found`
  - **Fix**: Reinstall Python from python.org and check **"Add Python to PATH"**.
- **Issue**: `COM port is busy / PermissionError`
  - **Fix**: Close Arduino Serial Monitor or Thonny IDE before starting `python main.py`.
- **Issue**: 3D Models not showing in browser
  - **Fix**: Run `python main.py` or `python server.py` rather than opening `index.html` directly from the file explorer (browsers require an HTTP server to load `.glb` 3D files due to CORS policy).
