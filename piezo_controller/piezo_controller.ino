// ==============================================================================
// AlphaMat - ESP32 5-Piezo Controller (Letters A, B, C, D, E)
// Hardware Setup:
//   • Letter 'A': Pin 32 (GPIO 32)
//   • Letter 'B': Pin 33 (GPIO 33)
//   • Letter 'C': Pin VP (GPIO 36 / SENSOR_VP)
//   • Letter 'D': Pin 34 (GPIO 34)
//   • Letter 'E': Pin 35 (GPIO 35)
//   • Visual Feedback: Onboard LED on Pin 2 (GPIO 2)
//
// Anti-False Trigger System:
//   • Automatic baseline calibration on startup measures the resting voltage
//     of each pin (e.g. Pin 33 & Pin 35 resting DC offset/noise).
//   • Triggers ONLY when physical pressure produces a sharp spike ABOVE baseline
//     (SPIKE_THRESHOLD = 350 counts).
//   • Physical press only (automatic selection is OFF).
//   • Transmits clean letter ('A', 'B', 'C', 'D', 'E') over USB Serial at 115200 baud.
// ==============================================================================

const int LED_PIN         = 2;    // Onboard ESP32 LED (GPIO 2) for visual feedback
const int SPIKE_THRESHOLD = 350;  // Must spike 350 counts ABOVE resting baseline (ignores resting noise)
const int DEBOUNCE_MS     = 400;  // Debounce time to prevent double-triggers on a single step

struct PiezoPad {
  char letter;
  int pin;
  const char* label;
  int baseline;                   // Resting baseline voltage measured at startup
  unsigned long lastTapTime;
};

// 5 Piezo Sensor Pads for Alphabets A through E
PiezoPad pads[] = {
  { 'A', 32, "GPIO 32",      0, 0 },
  { 'B', 33, "GPIO 33",      0, 0 },
  { 'C', 36, "GPIO 36 (VP)",  0, 0 },
  { 'D', 34, "GPIO 34",      0, 0 },
  { 'E', 35, "GPIO 35",      0, 0 }  // Pin 35 for Letter 'E'
};

const int NUM_PADS = sizeof(pads) / sizeof(pads[0]);

void setup() {
  Serial.begin(115200);

  // Initialize visual feedback LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  // Initialize all 5 piezo input pins
  for (int i = 0; i < NUM_PADS; i++) {
    pinMode(pads[i].pin, INPUT);
  }

  Serial.println("==================================================");
  Serial.println("  AlphaMat 5-Piezo Controller Ready (Letters A-E) ");
  Serial.println("  • Mode: PRESS ONLY (False-Trigger Protected)    ");
  Serial.println("  • Calibrating resting baselines...              ");

  // Calibrate resting baseline for all pins to eliminate continuous false triggers
  delay(500); // Allow ADC pins to settle
  for (int i = 0; i < NUM_PADS; i++) {
    long sum = 0;
    for (int s = 0; s < 30; s++) {
      sum += analogRead(pads[i].pin);
      delay(5);
    }
    pads[i].baseline = sum / 30;

    Serial.print("  • ");
    Serial.print(pads[i].label);
    Serial.print(" (Letter ");
    Serial.print(pads[i].letter);
    Serial.print(") Resting Baseline: ");
    Serial.println(pads[i].baseline);
  }

  Serial.println("  Calibration complete! System ready.");
  Serial.println("  • Pad A: Pin 32 (GPIO 32)");
  Serial.println("  • Pad B: Pin 33 (GPIO 33)");
  Serial.println("  • Pad C: Pin VP (GPIO 36 / SENSOR_VP)");
  Serial.println("  • Pad D: Pin 34 (GPIO 34)");
  Serial.println("  • Pad E: Pin 35 (GPIO 35)");
  Serial.println("==================================================");
}

void loop() {
  unsigned long now = millis();

  // Scans all 5 pads - triggers ONLY when physical hit spikes above resting baseline
  for (int i = 0; i < NUM_PADS; i++) {
    int sensorValue = analogRead(pads[i].pin);
    int spike = sensorValue - pads[i].baseline;

    // Triggers ONLY if physical pressure produces a sharp spike above resting baseline
    if (spike >= SPIKE_THRESHOLD) {
      if (now - pads[i].lastTapTime > DEBOUNCE_MS) {
        // Visual feedback LED ON
        digitalWrite(LED_PIN, HIGH);

        // Send single uppercase letter to Serial (e.g. "A", "B", "C", "D", "E")
        Serial.println(pads[i].letter);

        pads[i].lastTapTime = now;

        delay(60);
        digitalWrite(LED_PIN, LOW); // Visual feedback LED OFF

        // Wait until piezo vibration settles below threshold before next read
        int settleCount = 0;
        while ((analogRead(pads[i].pin) - pads[i].baseline) >= (SPIKE_THRESHOLD / 2) && settleCount < 25) {
          delay(10);
          settleCount++;
        }

        break; // Process one pad per scan cycle for ADC stability
      }
    }
  }

  delay(2); // Small delay for ADC stability
}
