int Xpin = A0;
int Ypin = A1;
int Spin = 2;
int Xval;
int Yval;
int Sval;
int dt = 200;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(Xpin, INPUT);
pinMode(Ypin, INPUT);
pinMode(Spin, INPUT);
digitalWrite(Spin, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  Xval = analogRead(Xpin);
  Yval = analogRead(Ypin);
  Sval = digitalRead(Spin);
  delay(dt);
  Serial.print("X Value = ");
  Serial.print(Xval);
  Serial.print(" Y Value = ");
  Serial.print(Yval);
  Serial.print(" The switch state is ");
  Serial.println(Sval);
}
