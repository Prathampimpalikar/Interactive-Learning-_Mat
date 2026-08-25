# 🧩 Interactive Learning Mat (AlphaMat)

An interactive educational learning system designed to make early childhood learning more **engaging, visual, and interactive**. The project combines a Python desktop application, educational datasets, 3D model visualization, and optional piezoelectric sensor interaction.

---

## 📌 Project Overview

**Interactive Learning Mat** is an educational platform designed to help children learn alphabets and identify associated objects through an interactive interface.

For example:
* **A → Ant** in Animal Mode 🐜
* **A → Apple** in Fruit Mode 🍎

The system provides an easy-to-use learning environment where children can select learning categories, view educational information, and explore corresponding 3D models.

The project also contains hardware-support components for detecting interactions through piezoelectric sensors connected to a microcontroller (Arduino / ESP32).

---

## 🎯 Objectives

* Make alphabet learning interactive and engaging.
* Help children associate letters with real-world objects.
* Provide separate **Animal** and **Fruit** learning modes.
* Display images and educational information.
* Provide interactive **3D model visualization** with WebXR Augmented Reality.
* Support piezoelectric sensor-based interaction.
* Provide a desktop-based learning interface.
* Provide a browser-based 3D model viewer.
* Create a foundation for future AI-based learning analytics.

---

## ✨ Key Features

### 🔤 Alphabet Learning
The application allows children to learn alphabets by connecting letters with objects (e.g., A → Ant, A → Apple).

### 🐾 Animal Mode & 🍎 Fruit Mode
Dedicated learning modes displaying the item's image, name, educational fact dossiers, and corresponding 3D model.

### 🧊 3D Model Studio & WebXR AR
Real-time 360° 3D model visualization powered by Google `<model-viewer>` with camera controls, auto-rotation, snapshot capture, and mobile WebXR Augmented Reality (AR) mode.

### 🎛️ Piezoelectric Sensor Support & Virtual Mat Simulator
Detect physical interaction with the learning mat using USB serial communication or explore using the built-in virtual 26-node mat simulator.

---

## 🏗️ System Architecture

```text
                ┌──────────────────────┐
                │   Interactive Mat    │
                └──────────┬───────────┘
                           │
                    Piezo Sensors
                           │
                           ▼
                ┌──────────────────────┐
                │ ESP / Arduino Layer  │
                └──────────┬───────────┘
                           │
                      Serial Data
                           │
                           ▼
                ┌──────────────────────┐
                │ Python Controller    │
                │ / Hardware Listener  │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Desktop / Web Server │
                │     Python App       │
                └──────────┬───────────┘
                           │
               ┌───────────┴────────────┐
               ▼                        ▼
        Animal Mode               Fruit Mode
               │                        │
               ▼                        ▼
             Ant                     Apple
               │                        │
               └──────────┬─────────────┘
                          ▼
                  3D Model Viewer
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python** | Main backend server, hardware listener, and desktop UI |
| **CustomTkinter** | Desktop graphical interface |
| **HTML5 & CSS3** | Browser-based interactive viewer and UI |
| **JavaScript** | Dynamic client logic, Web Speech API, and animations |
| **Google `<model-viewer>`** | Interactive 3D object and WebXR AR visualization |
| **Arduino / ESP32** | Sensor interaction and analog telemetry |
| **Piezoelectric Sensors** | Physical footstep pressure detection |
| **JSON / Excel** | Educational dataset and taxonomy data |
| **Firebase Realtime DB** | Optional cloud synchronization |
| **GitHub Pages** | Web deployment hosting |

---

## 🚀 Installation & Quick Start

> 📖 **Complete Documentation:** See [`REQUIREMENTS_AND_SETUP.md`](REQUIREMENTS_AND_SETUP.md) for full system requirements, hardware setup, and troubleshooting.

### 1. Clone the Repository
```bash
git clone https://github.com/Prathampimpalikar/Interactive-Learning-_Mat.git
cd Interactive-Learning-_Mat
```

### 2. Set Up Virtual Environment & Dependencies
```powershell
# Create & activate virtual environment (Windows)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python main.py
```

> **One-Click Launch (Windows)**: You can also double-click [`run.bat`](run.bat).

---

## 🌐 Live Web Access & GitHub Pages

The web platform is hosted at:
👉 **[https://prathampimpalikar.github.io/Interactive-Learning-_Mat/](https://prathampimpalikar.github.io/Interactive-Learning-_Mat/)**

---

## 🔐 Firebase

Firebase service-account credentials such as `firebase_key.json` should **not** be committed to GitHub. Keep private credentials only on trusted local machines.

---

## 👨‍💻 Developers

**Pratham Pimpalikar**
* GitHub: [Prathampimpalikar](https://github.com/Prathampimpalikar)
* Repository: [Interactive-Learning-_Mat](https://github.com/Prathampimpalikar/Interactive-Learning-_Mat)

---

## 📄 License

This project is developed for **educational and academic purposes**.
