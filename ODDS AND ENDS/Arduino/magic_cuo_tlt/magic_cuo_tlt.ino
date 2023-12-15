int detect1;
int detect2;
void setup() {
  // put your setup code here, to run once:
  pinMode(7, INPUT);
  pinMode(6, INPUT);
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  detect1 = digitalRead(7);
  detect2 = digitalRead(6);
  
  
  digitalWrite(5, detect1);
  digitalWrite(4, detect2);
}
