// Pin connections
int DataPin = 2;   // Connect to DS (serial data input) pin on the shift register
int ClockPin = 3;  // Connect to SHCP (clock) pin on the shift register
int LatchPin = 4;  // Connect to STCP (latch) pin on the shift register
byte Data = 0;

void setup()
{
  pinMode(DataPin, OUTPUT);
  pinMode(ClockPin, OUTPUT);
  pinMode(LatchPin, OUTPUT);
  
  // Initialize shift register
  shiftWriteAllLow();  // Set all outputs to low initially
  updateShiftRegister();  // Update the shift register outputs
}

void loop()
{
  illuminateLED(2);  // Illuminate the third LED
  delay(1000);
  clearAllLEDs();    // Turn off all LEDs
  delay(1000);
}

void shiftWrite(int Pin, boolean State)
{
  bitWrite(Data, Pin, State);
}

void updateShiftRegister()
{
  digitalWrite(LatchPin, LOW);
  shiftOut(DataPin, ClockPin, MSBFIRST, Data);
  digitalWrite(LatchPin, HIGH);  // Latch the shifted data
}

void shiftWriteAllLow()
{
  for (int i = 0; i < 8; i++) {
    shiftWrite(i, LOW);
  }
}

void illuminateLED(int ledIndex)
{
  clearAllLEDs();  // Turn off all LEDs
  shiftWrite(ledIndex, HIGH);  // Illuminate the specified LED
  updateShiftRegister();  // Update the shift register outputs
}

void clearAllLEDs()
{
  shiftWriteAllLow();  // Turn off all LEDs
  updateShiftRegister();  // Update the shift register outputs
}
