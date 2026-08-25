/*
  =============================================================================
  AlphaMat - Arduino Uno / Nano Piezo Serial Controller (Letter 'A' ONLY)
  =============================================================================
  Sends ONLY the clean letter 'A' over Serial so the software immediately 
  and automatically opens Alphabet 'A'.
  =============================================================================
*/

const int PIEZO_PIN      = A0;    // Piezo sensor on Analog Pin A0
const int THRESHOLD      = 50;    // Tap sensitivity (range 0 - 1023)
const int DEBOUNCE_MS    = 600;   // Debounce delay to prevent double triggers

void setup() {
  Serial.begin(9600);             // 9600 baud rate for Python software
  pinMode(PIEZO_PIN, INPUT);
}

void loop() {
  int sensorVal = analogRead(PIEZO_PIN);

  // When piezo is tapped, send ONLY letter 'A'
  if (sensorVal >= THRESHOLD) {
    Serial.println("A");          // Clean letter trigger
    delay(DEBOUNCE_MS);
  }

  delay(10);
}
