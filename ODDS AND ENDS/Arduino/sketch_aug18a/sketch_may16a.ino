int trigPin1 = 4;    // Trigger
int echoPin1 = 5;    // Echo
long duration1, duration2, cm1, cm2, inches;
#include <SPI.h>
#include <LoRa.h>
//YWROBOT
//Compatible with the Arduino IDE 1.0
//Library version:1.1
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,20,4);  // set the LCD address to 0x27 for a 16 chars and 2 line display

void setup() {
  lcd.init();                      // initialize the lcd 
  lcd.init();
 
  //Serial Port begin
  Serial.begin (9600);
  //Define inputs and outputs
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  while (!Serial);
    Serial.println("LoRa Sender");
  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}
 
void loop() {
  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  lcd.clear();
  digitalWrite(trigPin1, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin1, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin1, LOW);

 
  // Read the signal from the sensor: a HIGH pulse whose
  // duration is the time (in microseconds) from the sending
  // of the ping to the reception of its echo off of an object.
  pinMode(echoPin1, INPUT);
  duration1 = pulseIn(echoPin1, HIGH);
  // Convert the time into a distance
  cm1 = (duration1/2) / 29.1;
  Serial.print("Sending packet: ");
  LoRa.beginPacket();
  if (cm1 <= 50) {
    Serial.println(1);
    LoRa.print(1);
  }
  if (cm1 > 50) {
    Serial.println(0);
    LoRa.print(0);
  }
  // send packet
  LoRa.endPacket();
  // Print a message to the LCD.
  lcd.backlight();
  lcd.print("Distance: ");
  lcd.print(cm1);
  lcd.print(" cm");

  
  
  delay(250);
}
