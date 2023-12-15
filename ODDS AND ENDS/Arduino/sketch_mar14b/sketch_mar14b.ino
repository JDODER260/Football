// define pins and variables
int enaPin1 = 2;
int enaPin2 = 3;
int enaPin3 = 4;
int enaPin4 = 5;
// In Pins
int inPin11 = 22;
int inPin12 = 23;
int inPin21 = 25;
int inPin22 = 24;
int inPin31 = 26;
int inPin32 = 27;
int inPin41 = 29;
int inPin42 = 28;
// Trig Pins
int trigPin1 = 13;
int trigPin2 = 11;
int trigPin3 = 9;
int trigPin4 = 7;
// Echo Pins
int echoPin1 = 12;
int echoPin2 = 10;
int echoPin3 = 8;
int echoPin4 = 6;
int distance1;
int distance2;
int distance3;
int distance4;
int minimum_distance = 10; // minimum distance to avoid obstacles
int safe_distance = 30; // safe distance to keep from obstacles
int max_speed = 255; // maximum motor speed
int min_speed = 128; // minimum motor speed

void setup() {
Serial.begin(115200);
//start all pins to make so you can use them
//trig
pinMode(trigPin1, OUTPUT);
pinMode(trigPin2, OUTPUT);
pinMode(trigPin3, OUTPUT);
pinMode(trigPin4, OUTPUT);
//echo
pinMode(echoPin1, INPUT);
pinMode(echoPin2, INPUT);
pinMode(echoPin3, INPUT);
pinMode(echoPin4, INPUT);
//ena
pinMode(enaPin1, OUTPUT);
pinMode(enaPin2, OUTPUT);
pinMode(enaPin3, OUTPUT);
pinMode(enaPin4, OUTPUT);
//in
pinMode(inPin11, OUTPUT);
pinMode(inPin12, OUTPUT);
pinMode(inPin21, OUTPUT);
pinMode(inPin22, OUTPUT);
pinMode(inPin31, OUTPUT);
pinMode(inPin32, OUTPUT);
pinMode(inPin41, OUTPUT);
pinMode(inPin42, OUTPUT);
pinMode(50, OUTPUT);
}

void move_backward() {
  digitalWrite(inPin11, HIGH);
  digitalWrite(inPin12, LOW);
  analogWrite(enaPin1, max_speed);
  digitalWrite(inPin21, HIGH);
  digitalWrite(inPin22, LOW);
  analogWrite(enaPin2, max_speed);
  digitalWrite(inPin31, HIGH);
  digitalWrite(inPin32, LOW);
  analogWrite(enaPin3, max_speed);
  digitalWrite(inPin41, HIGH);
  digitalWrite(inPin42, LOW);
  analogWrite(enaPin4, max_speed);
}


void check_distance() {
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);
  distance1 = pulseIn(echoPin1, HIGH) / 58;
  digitalWrite(trigPin2, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);
  distance2 = pulseIn(echoPin2, HIGH) / 58;
  digitalWrite(trigPin3, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin3, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin3, LOW);
  distance3 = pulseIn(echoPin3, HIGH) / 58;
  digitalWrite(trigPin4, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin4, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin4, LOW);
  distance4 = pulseIn(echoPin4, HIGH) / 58;

Serial.print("Front distance: ");
Serial.print(distance1);
Serial.print(" cm\tBack distance: ");
Serial.print(distance2);
Serial.print(" cm\tRight distance: ");
Serial.print(distance3);
Serial.print(" cm\tLeft distance: ");
Serial.print(distance4);
Serial.println(" cm");
}

void avoid_obstacle() {
if (distance1 <= minimum_distance) { // if something is in front, backup a little and turn 
  Serial.println("Going back");
  move_backward(); 
  delay(500);
}

}

void loop() {
digitalWrite(50, HIGH);
// measure distance from all four sensors
check_distance();

// avoid obstacles
avoid_obstacle();

}
