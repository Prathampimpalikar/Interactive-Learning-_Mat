#include <WiFi.h>
#include <HTTPClient.h>

// =====================================================
// WIFI
// =====================================================

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// =====================================================
// FIREBASE
// =====================================================

// IMPORTANT:
// Use your actual Firebase Realtime Database URL.
const char* FIREBASE_URL =
  "https://interactive-learning-mat-default-rtdb.firebaseio.com";

// =====================================================
// PIEZO PINS
// =====================================================

#define PIEZO_A 5
#define PIEZO_B 4
#define PIEZO_C 14
#define PIEZO_D 12

// =====================================================
// VARIABLES
// =====================================================

unsigned long lastPressTime = 0;

const unsigned long debounceTime = 1000;


// =====================================================
// SETUP
// =====================================================

void setup() {

  Serial.begin(115200);

  delay(1000);

  Serial.println();
  Serial.println("================================");
  Serial.println(" INTERACTIVE LEARNING MAT");
  Serial.println(" ESP32 PIEZO CONTROLLER");
  Serial.println("================================");

  // Piezo pins
  pinMode(PIEZO_A, INPUT);
  pinMode(PIEZO_B, INPUT);
  pinMode(PIEZO_C, INPUT);
  pinMode(PIEZO_D, INPUT);

  // Connect WiFi
  connectWiFi();
}


// =====================================================
// WIFI CONNECTION
// =====================================================

void connectWiFi() {

  Serial.println();
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi Connected!");

  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());
}


// =====================================================
// SEND LETTER TO FIREBASE
// =====================================================

void sendLetter(String letter) {

  if (WiFi.status() != WL_CONNECTED) {

    Serial.println("WiFi disconnected.");

    connectWiFi();
  }

  HTTPClient http;

  String url = String(FIREBASE_URL) +
               "/admin/currentLetter.json";

  Serial.println();
  Serial.println("Sending letter: " + letter);
  Serial.println("Firebase URL:");
  Serial.println(url);

  http.begin(url);

  http.addHeader(
    "Content-Type",
    "application/json"
  );

  // Firebase needs JSON string
  String jsonData = "\"" + letter + "\"";

  int httpResponseCode =
    http.PUT(jsonData);

  Serial.print("Firebase Response: ");
  Serial.println(httpResponseCode);

  if (httpResponseCode > 0) {

    String response =
      http.getString();

    Serial.println("Firebase reply:");
    Serial.println(response);

  } else {

    Serial.print("Firebase Error: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}


// =====================================================
// CHECK PIEZO
// =====================================================

void checkPiezo() {

  // ---------------------------------
  // PIEZO A
  // ---------------------------------

  if (digitalRead(PIEZO_A) == HIGH) {

    if (millis() - lastPressTime > debounceTime) {

      Serial.println("PIEZO 1 PRESSED → LETTER A");

      sendLetter("A");

      lastPressTime = millis();
    }
  }


  // ---------------------------------
  // PIEZO B
  // ---------------------------------

  else if (digitalRead(PIEZO_B) == HIGH) {

    if (millis() - lastPressTime > debounceTime) {

      Serial.println("PIEZO 2 PRESSED → LETTER B");

      sendLetter("B");

      lastPressTime = millis();
    }
  }


  // ---------------------------------
  // PIEZO C
  // ---------------------------------

  else if (digitalRead(PIEZO_C) == HIGH) {

    if (millis() - lastPressTime > debounceTime) {

      Serial.println("PIEZO 3 PRESSED → LETTER C");

      sendLetter("C");

      lastPressTime = millis();
    }
  }


  // ---------------------------------
  // PIEZO D
  // ---------------------------------

  else if (digitalRead(PIEZO_D) == HIGH) {

    if (millis() - lastPressTime > debounceTime) {

      Serial.println("PIEZO 4 PRESSED → LETTER D");

      sendLetter("D");

      lastPressTime = millis();
    }
  }
}


// =====================================================
// LOOP
// =====================================================

void loop() {

  checkPiezo();

  delay(50);
}
