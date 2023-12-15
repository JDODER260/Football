// define pins and variables
int ena1 = 2;
int in11 = 22;
int in12 = 23;
int ena2 = 3;
int in21 = 25;
int in22 = 24;
int ena3 = 4;
int in31 = 26;
int in32 = 27;
int ena4 = 5;
int in41 = 29;
int in42 = 28;
const int trigPin1 = 13;
const int echoPin1 = 12;
const int trigPin2 = 11;
const int echoPin2 = 10;
const int trigPin3 = 9;
const int echoPin3 = 8;
const int trigPin4 = 7;
const int echoPin4 = 6;
int front;
int back;
int right;
int left;
int duration1, duration2, duration3, duration4;
int minimum_distance = 20; // minimum distance to avoid obstacles
int safe_distance = 50; // safe distance to keep from obstacles
int max_speed = 255; // maximum motor speed
int min_speed = 128; // minimum motor speed

void setup() {
  Serial.begin(9600);
  pinMode(trigPin1, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin1, INPUT); // Sets the echoPin as an Input
  pinMode(trigPin2, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin2, INPUT); // Sets the echoPin as an Input
  pinMode(trigPin3, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin3, INPUT); // Sets the echoPin as an Input
  pinMode(trigPin4, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin4, INPUT); // Sets the echoPin as an Input
  pinMode(ena1, OUTPUT);
  pinMode(in11, OUTPUT);
  pinMode(in12, OUTPUT);
  pinMode(ena2, OUTPUT);
  pinMode(in21, OUTPUT);
  pinMode(in22, OUTPUT);
  pinMode(ena3, OUTPUT);
  pinMode(in31, OUTPUT);
  pinMode(in32, OUTPUT);
  pinMode(ena4, OUTPUT);
  pinMode(in41, OUTPUT);
  pinMode(in42, OUTPUT);
  pinMode(50, OUTPUT);
}

void full_ahead() {
  
  digitalWrite(in11,HIGH);
  digitalWrite(in12,LOW);
  digitalWrite(in21,HIGH);
  digitalWrite(in22,LOW); 
  digitalWrite(in31,HIGH);
  digitalWrite(in32,LOW);
  digitalWrite(in41,HIGH);
  digitalWrite(in42,LOW);
  delay(100);
}
int measure_distance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  return duration * 0.034 / 2;
}

void full_backwards() {
  digitalWrite(in11,LOW);
  digitalWrite(in12,HIGH);
  digitalWrite(in21,LOW);
  digitalWrite(in22,HIGH); 
  digitalWrite(in31,LOW);
  digitalWrite(in32,HIGH);
  digitalWrite(in41,LOW);
  digitalWrite(in42,HIGH);
  delay(100);
}

void half_ahead() {
  digitalWrite(in11,HIGH);
  digitalWrite(in12,LOW);
  digitalWrite(in21,HIGH);
  digitalWrite(in22,LOW); 
  digitalWrite(in31,HIGH);
  digitalWrite(in32,LOW);
  digitalWrite(in41,HIGH);
  digitalWrite(in42,LOW);
  delay(100);
}

void half_backwards() {
  digitalWrite(in11,LOW);
  digitalWrite(in12,HIGH);
  digitalWrite(in21,LOW);
  digitalWrite(in22,HIGH);
  digitalWrite(in31,LOW);
  digitalWrite(in32,HIGH);
  digitalWrite(in41,LOW);
  digitalWrite(in42,HIGH);
  delay(100);
}
void stop() {
  digitalWrite(in11, LOW);
  digitalWrite(in12, LOW);
  digitalWrite(in21, LOW);
  digitalWrite(in22, LOW);
  digitalWrite(in31, LOW);
  digitalWrite(in32, LOW);
  digitalWrite(in41, LOW);
  digitalWrite(in42, LOW);
}



void turn_left() {
digitalWrite(in11, HIGH);
digitalWrite(in12, LOW);
digitalWrite(in21, LOW);
digitalWrite(in22, HIGH);
digitalWrite(in31, HIGH);
digitalWrite(in32, LOW);
digitalWrite(in41, LOW);
digitalWrite(in42, HIGH);
}

void turn_right() {
digitalWrite(in11, LOW);
digitalWrite(in12, HIGH);
digitalWrite(in21, HIGH);
digitalWrite(in22, LOW);
digitalWrite(in31, LOW);
digitalWrite(in32, HIGH);
digitalWrite(in41, HIGH);
digitalWrite(in42, LOW);
}

void check_distance() {
// measure front distance
digitalWrite(trigPin1, LOW);
delayMicroseconds(2);
digitalWrite(trigPin1, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin1, LOW);
front = pulseIn(echoPin1, HIGH) / 58;

// measure back distance
digitalWrite(trigPin2, LOW);
delayMicroseconds(2);
digitalWrite(trigPin2, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin2, LOW);
back = pulseIn(echoPin2, HIGH) / 58;

// measure right distance
digitalWrite(trigPin3, LOW);
delayMicroseconds(2);
digitalWrite(trigPin3, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin3, LOW);
right = pulseIn(echoPin3, HIGH) / 58;

// measure left distance
digitalWrite(trigPin4, LOW);
delayMicroseconds(2);
digitalWrite(trigPin4, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin4, LOW);
left = pulseIn(echoPin4, HIGH) / 58;

Serial.print("Front distance: ");
Serial.print(front);
Serial.print(" cm\tBack distance: ");
Serial.print(back);
Serial.print(" cm\tRight distance: ");
Serial.print(right);
Serial.print(" cm\tLeft distance: ");
Serial.print(left);
Serial.println(" cm");
}


void loop() {
  digitalWrite(ena1, HIGH);
  digitalWrite(ena2, HIGH);
  digitalWrite(ena3, HIGH);
  digitalWrite(ena4, HIGH);
  digitalWrite(50, HIGH);
  int front = measure_distance(trigPin1, echoPin1);
  int back = measure_distance(trigPin2, echoPin2);
  int right = measure_distance(trigPin3, echoPin3);
  int left = measure_distance(trigPin4, echoPin4);
  
  Serial.print("Front distance: ");
  Serial.print(front);
  Serial.print("cm, Back distance: ");
  Serial.print(back);
  Serial.print("cm, Right distance: ");
  Serial.print(right);
  Serial.print("cm, Left distance: ");
  Serial.print(left);
  Serial.println("cm");
  if (front < 10 ) {
    Serial.print("Stoped");
    analogWrite(ena1, 0);
    analogWrite(ena2, 0);  
    analogWrite(ena3, 0);
    analogWrite(ena4, 0);
    delay(2000);
  }
  if (front >= 100) {
    Serial.println("Full ahead");
    full_ahead();
  } else if (front < 100 && front > 40) {
    Serial.println("Half ahead");
    half_ahead();
  } else if (front < 40 && left < 40 && right < 40 && back > 50) {
    Serial.println("full bakwards");
    full_backwards();
  } else if(front < 40 && left < 60 && right < 60 && back < 100 && back > 40) {
    Serial.println("Half backwards");
    half_backwards();
  } else if (front < 40 && right >= 60) {
    Serial.println("turn right");
    turn_right();
  } else if (front < 40 && left >= 60) {
    Serial.println("turn left");
    turn_left();
  } else {
    analogWrite(ena1, 0);
    analogWrite(ena2, 0);  
    analogWrite(ena3, 0);
    analogWrite(ena4, 0);
  }
  delay(500);
 
} 
