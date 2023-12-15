int Xpin = A0;
int Ypin = A1;
int Spin = 2;
int Xval, Yval, Sval;
int dt = 200;

int latchPin = 11;
int clockPin = 9;
int dataPin = 12;

void setup() {
  Serial.begin(9600);
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(Xpin, INPUT);
  pinMode(Ypin, INPUT);
  pinMode(Spin, INPUT);
  digitalWrite(Spin, HIGH);
}

void loop() {
  Xval = analogRead(Xpin);
  Yval = analogRead(Ypin);
  Sval = digitalRead(Spin);
  
  digitalWrite(latchPin, LOW);
  
  if (Xval > 336 && Xval < 506) {
    shiftOut(dataPin, clockPin, LSBFIRST, byte(0b00100000)); // Pattern 2
    Serial.println("this is no2");
  } else if (Xval >= 512 && Xval <= 680) {
    shiftOut(dataPin, clockPin, LSBFIRST, byte(0b00000100)); // Pattern 3
    Serial.println("this is no3");
  } else if (Xval >= 680 && Xval <= 852) {
    shiftOut(dataPin, clockPin, LSBFIRST, byte(0b00000010)); // Pattern 3
    Serial.println("this is no3");
  } else if (Xval >= 852 && Xval <= 1023) {
    shiftOut(dataPin, clockPin, LSBFIRST, byte(0b00000001)); // Pattern 3end
    Serial.println("this is no3");
  } else if (Xval > 164 && Xval < 336) {
    shiftOut(dataPin, clockPin, LSBFIRST, byte(0b01000000)); // Pattern 2
    Serial.println("this is no2");
  } else if (Xval >= 0 && Xval < 164) {
    shiftOut(dataPin, clockPin, LSBFIRST, byte(0b10000000)); // Pattern 2
    Serial.println("this is no2");
  } else {
    shiftOut(dataPin, clockPin, LSBFIRST, byte(0b00011000)); // Pattern 1
    Serial.println("this is no1");
  }
  
  digitalWrite(latchPin, HIGH);

  delay(dt);

  Serial.print("X Value = ");
  Serial.print(Xval);
  Serial.print(" Y Value = ");
  Serial.print(Yval);
  Serial.print(" The switch state is ");
  Serial.println(Sval);
}
