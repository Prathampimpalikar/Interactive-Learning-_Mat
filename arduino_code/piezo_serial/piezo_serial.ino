/*
  =============================================================================
  AlphaMat - ESP32 Single Piezo Controller (Alphabet 'A' ONLY)
  =============================================================================
  Sends ONLY the clean letter 'A' over Serial & Firebase so the software 
  immediately and automatically opens Alphabet 'A'.
  =============================================================================
*/

#include <WiFi.h>
#include <HTTPClient.h>

const char* WIFI_SSID     = "Airtel_Nishka";
const char* WIFI_PASSWORD = "Nishka@123";
const char* FIREBASE_URL  = "https://interactive-mat-b38b8-default-rtdb.firebaseio.com/admin/currentLetter.json";

const int PIEZO_PIN       = 32;   // GPIO 32 for Alphabet 'A'
const int THRESHOLD       = 100;  // Sensitivity threshold (0-4095)
const int DEBOUNCE_MS     = 600;  // Debounce delay

void sendLetterToFirebase(String letter) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(FIREBASE_URL);
    http.addHeader("Content-Type", "application/json");
    String payload = "\"" + letter + "\"";
    http.PUT(payload);
    http.end();
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(PIEZO_PIN, INPUT);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(400);
    attempts++;
  }
}

void loop() {
  int sensorValue = analogRead(PIEZO_PIN);

  if (sensorValue >= THRESHOLD) {
    // Send clean 'A' to Serial for local Python software
    Serial.println("A");

    // Send 'A' to Firebase for web app
    sendLetterToFirebase("A");

    delay(DEBOUNCE_MS);
  }

  delay(10);
}
