int DataPin = 2;
int ClockPin = 3;
int LatchPin = 4;
byte Data = 0;

void setup()
{
  pinMode(DataPin, OUTPUT);
  pinMode(ClockPin, OUTPUT);
  pinMode(LatchPin, OUTPUT);
}

void loop()
{
  crazyPattern(); // Call your new complex LED pattern
  delay(1000);    // Delay between patterns
}

// Function to create a complex LED pattern
void crazyPattern()
{
  for (int i = 0; i < 5; i++) {
    shiftWrite(i, HIGH);     // Turn on the i-th LED
    delay(100);
    shiftWrite(i, LOW);      // Turn off the i-th LED
  }

  for (int j = 7; j >= 0; j--) {
    shiftWrite(j, HIGH);     // Turn on the j-th LED
    delay(100);
    shiftWrite(j, LOW);      // Turn off the j-th LED
  }

  AllHigh();  // Turn on all LEDs
  delay(500);
  AllLow();   // Turn off all LEDs
  delay(500);

  for (int k = 0; k < 3; k++) {
    for (int l = 0; l < 8; l++) {
      shiftWrite(l, HIGH);   // Turn on the l-th LED
      delay(50);
      shiftWrite(l, LOW);    // Turn off the l-th LED
    }
    delay(200);
  }

  for (int m = 7; m >= 0; m--) {
    for (int n = 0; n < 8; n++) {
      shiftWrite(n, HIGH);   // Turn on the n-th LED
      delay(50);
      shiftWrite(n, LOW);    // Turn off the n-th LED
    }
    delay(200);
  }
}

// Rest of the functions remain unchanged
void shiftWrite(int Pin, boolean State)
{
  bitWrite(Data, Pin, State);
  shiftOut(DataPin, ClockPin, MSBFIRST, Data);
  digitalWrite(LatchPin, HIGH);
  digitalWrite(LatchPin, LOW);
}

void AllHigh()
{
  for (int PinNo = 0; PinNo < 8; PinNo++) {
    shiftWrite(PinNo, HIGH);
  }
}

void AllLow()
{
  for (int PinNo = 0; PinNo < 8; PinNo++) {
    shiftWrite(PinNo, LOW);
  }
}

void SOS()
{
  for (int x = 0; x < 10; x++) {
    AllHigh();
    delay(500);
    AllLow();
    delay(500);
  }
}
