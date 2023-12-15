const int analogPin = A0;   // Connect trimmer's middle pin to analog pin A0

void setup() {
  Serial.begin(9600);
}

void loop() {
  int trimmerValue = analogRead(analogPin);
  Serial.println(trimmerValue);
  delay(100);  // Adjust the delay as needed
}
