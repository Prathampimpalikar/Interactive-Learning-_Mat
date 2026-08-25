/*
  =============================================================================
  AlphaMat - ESP32 Single Piezo Sensor Controller (GPIO 32 -> Letter 'A')
  =============================================================================
  Hardware Setup:
    - Piezo Signal Wire -> ESP32 GPIO 32 (Analog Input)
    - Piezo Ground Wire -> ESP32 GND
    - (Optional) 1M Ohm parallel resistor between GPIO 32 and GND for stability

  Behavior:
    - Sends clean letter "A" over Serial at 115200 baud when piezo is pressed.
    - Uses threshold detection with debounce logic to prevent double triggers.
  =============================================================================
*/

// Configuration
const int PIEZO_PIN   = 32;    // GPIO 32 for Letter 'A'
const int THRESHOLD   = 150;   // Sensitivity threshold (adjust higher/lower if needed)
const int DEBOUNCE_MS = 400;   // Debounce delay in milliseconds

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);    // 12-bit resolution (0-4095) on ESP32

  // Optional startup ready signal
  Serial.println("ESP32 READY");
}

void loop() {
  int value = analogRead(PIEZO_PIN);

  // Trigger when piezo hit exceeds threshold
  if (value > THRESHOLD) {
    // Send clean 'A' to Python hardware listener
    Serial.println("A");

    // Wait debounce period
    delay(DEBOUNCE_MS);

    // Wait until piezo vibration settles below threshold
    while (analogRead(PIEZO_PIN) > THRESHOLD) {
      delay(10);
    }
  }

  delay(10);
}
