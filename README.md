# 🧩 Interactive Learning Mat

An interactive educational learning system designed to make early childhood learning more **engaging, visual, and interactive**. The project combines a Python desktop application, educational datasets, 3D model visualization, and optional piezoelectric sensor interaction.

## 📌 Project Overview

**Interactive Learning Mat** is an educational platform designed to help children learn alphabets and identify associated objects through an interactive interface.

For example:

* **A → Ant** in Animal Mode 🐜
* **A → Apple** in Fruit Mode 🍎

The system provides an easy-to-use learning environment where children can select learning categories, view educational information, and explore corresponding 3D models.

The project also contains hardware-support components for detecting interactions through piezoelectric sensors connected to a microcontroller.

---

## 🎯 Objectives

* Make alphabet learning interactive and engaging.
* Help children associate letters with real-world objects.
* Provide separate **Animal** and **Fruit** learning modes.
* Display images and educational information.
* Provide interactive **3D model visualization**.
* Support piezoelectric sensor-based interaction.
* Provide a desktop-based learning interface.
* Provide a browser-based 3D model viewer.
* Create a foundation for future AI-based learning analytics.

---

## ✨ Key Features

### 🔤 Alphabet Learning

The application allows children to learn alphabets by connecting letters with objects.

Example:

**A → Ant**
**A → Apple**

### 🐾 Animal Mode

Animal Mode displays objects associated with the selected alphabet.

Example:

> A → Ant

The application can display the animal's image, name, and corresponding 3D model.

### 🍎 Fruit Mode

Fruit Mode provides fruit-based learning.

Example:

> A → Apple

The child can view the fruit image, name, and 3D model.

### 🧊 3D Model Viewer

The project includes a browser-based 3D viewer for interactive visualization of educational models.

3D assets are stored inside the project and can be displayed through the web interface.

### 🎛️ Piezoelectric Sensor Support

The project contains Arduino/ESP-based code and Python controller/listener components for interacting with piezoelectric sensors.

The sensor system can be used to detect physical interaction with the learning mat.

### 🖥️ Desktop Application

The main learning application is implemented using Python and provides a desktop interface for interacting with the learning system.

### 🌐 Browser-Based Viewer

A separate browser interface is available for viewing the 3D educational models.

**Live Viewer:**

https://prathampimpalikar.github.io/Interactive-Learning-_Mat/

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
                │ Desktop Application  │
                │     Python GUI       │
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

| Technology                | Purpose                          |
| ------------------------- | -------------------------------- |
| **Python**                | Main application development     |
| **CustomTkinter**         | Desktop graphical interface      |
| **HTML**                  | Browser-based viewer             |
| **JavaScript**            | Interactive web functionality    |
| **3D / GLB Models**       | Interactive object visualization |
| **Arduino / ESP**         | Sensor interaction               |
| **Piezoelectric Sensors** | Physical interaction detection   |
| **JSON**                  | Dataset and application data     |
| **Git & GitHub**          | Version control                  |
| **GitHub Pages**          | Web deployment                   |
| **Firebase**              | Optional backend integration     |

---

## 📂 Project Structure

```text
Interactive-Learning-_Mat/
│
├── .github/
│   └── workflows/
│
├── arduino_code/
│   └── piezo_serial/
│
├── dataset/
│
├── html/
│
├── images/
│
├── model/
│
├── piezo_controller/
│
├── FIREBASE.JSON
├── boot.py
├── build.bat
├── category.py
├── dashboard.py
├── dataset.json
├── excel_reader.py
├── firebase.py
├── firebase_config.py
├── hardware_listener.py
├── index.html
├── letter.py
├── login.py
├── main.py
├── piezo_controller.py
├── requirements.txt
├── run.bat
├── selection.py
├── server.py
├── test.py
├── test_firebase.py
├── viewer.py
└── README.md
```

The current repository contains these major components, including Arduino code, datasets, HTML files, images, models, Python application files, and deployment configuration.

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Prathampimpalikar/Interactive-Learning-_Mat.git
```

### 2. Enter the Project Directory

```bash
cd Interactive-Learning-_Mat
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python main.py
```

These are also the setup commands currently documented in the repository.

---

## 🌐 Run the 3D Viewer

The browser-based viewer can be accessed through the deployed GitHub Pages website:

```text
https://prathampimpalikar.github.io/Interactive-Learning-_Mat/
```

GitHub Pages hosts the browser viewer and static 3D assets, while the CustomTkinter desktop application runs locally using Python.

---

## 📊 Dataset

The project contains educational data used to associate alphabets with learning objects.

Example:

```json
{
    "letter": "A",
    "animal": "Ant",
    "fruit": "Apple"
}
```

The dataset can be expanded to support the complete alphabet from **A–Z**.

---

## 🧊 3D Models

The project supports `.glb` 3D models for educational objects.

Example:

```text
model/
├── ant.glb
└── apple.glb
```

These models can be displayed through the browser-based 3D viewer.

---

## 🔌 Hardware Integration

The project contains a hardware interaction layer using piezoelectric sensors.

Basic workflow:

```text
Piezo Sensor
     ↓
ESP / Arduino
     ↓
Serial Communication
     ↓
Python Hardware Listener
     ↓
Learning Application
     ↓
Educational Content
```

This allows physical interaction with the learning mat to be connected with the software application.

---

## 🔐 Firebase

The repository contains Firebase-related files for backend integration.

**Important:** Firebase service-account credentials such as `firebase_key.json` should **not** be uploaded to GitHub.

Keep private credentials only on trusted local machines. The repository itself currently notes that the Firebase service-account file is intentionally ignored.

---

## 📱 Future Enhancements

The project can be extended with:

* 🤖 AI-based personalized learning
* 📈 Student progress tracking
* 📊 Learning analytics dashboard
* 🧠 AI-generated learning suggestions
* 👨‍🏫 Teacher dashboard
* 👨‍👩‍👧 Parent progress monitoring
* 🔤 Complete A–Z learning content
* 🐶 More animal categories
* 🍊 More fruit categories
* 🎮 Gamification
* 🔊 Audio pronunciation
* 👁️ Computer vision-based interaction
* ☁️ Cloud-based data storage
* 📱 Mobile application
* 🏆 Student achievement system

---

## 👨‍💻 Developers

**Pratham Pimpalikar**

GitHub:
https://github.com/Prathampimpalikar

Project Repository:
https://github.com/Prathampimpalikar/Interactive-Learning-_Mat

---

## 📜 Project Status

🚧 **Currently under development**

The current version provides the core learning interface, educational content, 3D model viewer, Python application components, and hardware-support components. The system can be further expanded into a complete AI-powered interactive learning platform.

---

## ⭐ Contribution

Contributions, suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Commit your changes.
5. Push the branch.
6. Create a Pull Request.

---

## 📄 License

This project is developed for **educational and academic purposes**.

---

### ⭐ Interactive Learning Mat

**Making Learning More Interactive, Visual, and Engaging.**
