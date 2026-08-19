/*
  Interactive Learning Mat - Piezo Sensor Serial Trigger
  
  This code reads a piezo sensor connected to Analog Pin A0.
  When a tap is detected (voltage spike exceeds the threshold),
  it sends the letter 'a' over Serial to trigger the application.
*/

const int PIEZO_PIN = A0;      // Analog pin connected to piezo
const int THRESHOLD = 50;      // Tap sensitivity threshold (adjust between 10 and 200)
const int DEBOUNCE_DELAY = 300; // Delay to prevent double-triggers (milliseconds)

void setup() {
  Serial.begin(9600);          // Initialize serial communication at 9600 bps
}

void loop() {
  int sensorValue = analogRead(PIEZO_PIN);

  if (sensorValue >= THRESHOLD) {
    // Piezo sensor was tapped
    Serial.println("a");       // Send letter 'a' to Python
    delay(DEBOUNCE_DELAY);     // Wait to ignore mechanical vibration bounce
  }
}
