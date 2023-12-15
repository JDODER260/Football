const int analogPin = A0;   // Connect trimmer's middle pin to analog pin A0
int latchPin = 11;
int clockPin = 9;
int dataPin = 12;

void setup() {
  Serial.begin(9600);
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
}

void loop() {
    int trimmerValue = analogRead(analogPin);
  Serial.println(trimmerValue);
  delay(100);  // Adjust the delay as needed
  byte patterns[] = {
  0x01, 0x03, 0x05, 0x09,
  0x11, 0x21, 0x41, 0x81,
  0x41, 0x21, 0x11, 0x09,
  0x05, 0x03, 0x07, 0x0B,
  0x13, 0x23, 0x43, 0x83,
  0x43, 0x23, 0x13, 0x0B,
  0x07, 0x0F, 0x17, 0x27,
  0x47, 0x87, 0x47, 0x27,
  0x17, 0x0F, 0x1F, 0x2F,
  0x4F, 0x8F, 0x4F, 0x2F,
  0x1F, 0x3F, 0x5F, 0x9F,
  0x5F, 0x3F, 0x7F, 0xBF,
  0x7F, 0xFF,
  0x92, 0x49, 0x24, 0x49, 0x92, // Diamond
  0x18, 0x3C, 0x7E, 0x3C, 0x18, // Hourglass
  0xC3, 0x99, 0x24, 0x99, 0xC3, // X-shape
  0x81, 0x42, 0x24, 0x18, 0x18, // Arrow
  0x0C, 0x12, 0x21, 0x12, 0x0C, // Cross
  0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, // Checkerboard
  0xF0, 0xF0, 0x0F, 0x0F, 0xF0, 0xF0, 0x0F, 0x0F, // Diagonal split
  0x18, 0x3C, 0x7E, 0xFF, 0x18, 0x3C, 0x7E, 0xFF, // Gradual brightness
  0x81, 0xC3, 0xE7, 0xFF, 0xFF, 0xE7, 0xC3, 0x81, // Alternating brightness
  0x01, 0x07, 0x1F, 0x7F, 0x7F, 0x1F, 0x07, 0x01, // Expanding and contracting
  0xC1, 0xE3, 0xF7, 0xFF, 0xFF, 0xF7, 0xE3, 0xC1, // Alternating colors
  0x99, 0x5A, 0x24, 0x18, 0x18, 0x24, 0x5A, 0x99, // Custom pattern 1
  0x66, 0xC3, 0xE7, 0xDB, 0xDB, 0xE7, 0xC3, 0x66, // Custom pattern 2
  0x00, 0x08, 0x3E, 0x1C, 0x08, 0x00, 0x08, 0x00, // Arrow blinking
  0x08, 0x1C, 0x3E, 0x08, 0x1C, 0x3E, 0x08, 0x1C,  // Alternating arrows
  0x0E, 0x1C, 0x38, 0x70, 0x38, 0x1C, 0x0E, 0x00, // Triangle growing and shrinking
  0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01, // Chase effect
  0x00, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x7E, 0x00, // Middle bar
  0x7E, 0x7E, 0x7E, 0x7E, 0x00, 0x7E, 0x7E, 0x7E, // Cross expand and contract
  0x11, 0x22, 0x44, 0x88, 0x44, 0x22, 0x11, 0x00, // Diagonal waves
  0x00, 0x7E, 0x63, 0x5D, 0x5D, 0x63, 0x7E, 0x00, // Custom pattern 3
  0x00, 0x10, 0x38, 0x7C, 0x7C, 0x38, 0x10, 0x00, // Hourglass blinking
  0x24, 0x24, 0x24, 0x5A, 0x5A, 0x42, 0x42, 0x81, // Custom pattern 4
  0x7E, 0x3C, 0x18, 0x18, 0x18, 0x18, 0x3C, 0x7E, // Inverse triangle growing and shrinking
  0x00, 0x00, 0x7E, 0x00, 0x00, 0x00, 0x7E, 0x00,  // Vertical bar
  0x55, 0xAA, 0x00, 0xFF, 0x33, 0xCC, 0x88, 0x22, // Random pattern 1
  0x0F, 0xF0, 0x3C, 0xC3, 0x7E, 0x81, 0x1E, 0xE1, // Random pattern 2
  0x9A, 0x75, 0x56, 0x69, 0x34, 0x4B, 0xA8, 0xD7, // Random pattern 3
  0xC6, 0x12, 0xA5, 0x3F, 0x78, 0xE9, 0x5C, 0xAB, // Random pattern 4
  0x6D, 0x1A, 0x47, 0x8C, 0x3B, 0x9E, 0x54, 0xF1, // Random pattern 5
  0x2A, 0x57, 0x8C, 0x1F, 0x6B, 0xE4, 0x3D, 0x90, // Random pattern 6
  0x77, 0xAA, 0x88, 0x11, 0x44, 0x99, 0x22, 0xEE, // Random pattern 7
  0xB4, 0xD3, 0x6F, 0x1C, 0x87, 0xE2, 0x9A, 0x56, // Random pattern 8
  0x98, 0x35, 0x7A, 0xBD, 0x61, 0xEC, 0x4F, 0xA2, // Random pattern 9
  0xDB, 0x26, 0x5C, 0x91, 0x38, 0x74, 0xE9, 0x1A  // Random pattern 10
};

  // Loop through the first pattern going forwards
  for (int i = 0; i < 50; i++) {
    digitalWrite(latchPin, LOW);
    shiftOut(dataPin, clockPin, LSBFIRST, patterns[i]);
    digitalWrite(latchPin, HIGH);

    delay(100); // Adjust speed for better visibility
  }

  // Loop through the first pattern going backwards
  for (int i = 49; i >= 0; i--) {
    digitalWrite(latchPin, LOW);
    shiftOut(dataPin, clockPin, LSBFIRST, patterns[i]);
    digitalWrite(latchPin, HIGH);

    delay(100); // Adjust speed for better visibility
  }

  // Loop through the rest of the patterns
  for (int i = 50; i < sizeof(patterns); i++) {
    digitalWrite(latchPin, LOW);
    shiftOut(dataPin, clockPin, LSBFIRST, patterns[i]);
    digitalWrite(latchPin, HIGH);

    delay(150); // Adjust speed for better visibility
  }

  delay(1000); // Delay between complete cycles

}