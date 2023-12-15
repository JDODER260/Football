int detect1;
int detect2;
void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  pinMode(7, INPUT);
  pinMode(6, INPUT);
  pinMode(5, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(13, OUTPUT);
  digitalWrite(13, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  detect1 = digitalRead(6);
  detect2 = digitalRead(7);
  
  Serial.print(detect1);
  Serial.print(", ");
  Serial.println(detect2);
  digitalWrite(5, detect1);
  digitalWrite(8, detect1);
  digitalWrite(4, detect2);
  digitalWrite(9, detect2); 
}
