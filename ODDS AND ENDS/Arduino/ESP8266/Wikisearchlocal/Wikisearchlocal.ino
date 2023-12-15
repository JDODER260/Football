#include <Arduino.h>

char ssid[] = "FORBLYNK";
char pass[] = "kilbrack087";

void setup() {
  // Debug console
  Serial.begin(115200);

  // Set ESP8266 baud rate
  Serial3.begin(115200);
  delay(10);

  // Connect to WiFi
  Serial3.println("AT+CWJAP=\"" + String(ssid) + "\",\"" + String(pass) + "\"");
  delay(5000); // Wait for WiFi connection

  // Fetch Wikipedia page from ESP8266
  Serial3.println("AT+CIPSTART=\"TCP\",\"en.wikipedia.org\",80");
  delay(1000);
  Serial3.println("AT+CIPSEND=" + String(wikipediaGetRequest.length()));
  delay(1000);
  Serial3.print(wikipediaGetRequest);
}

void loop() {
  if (Serial3.available()) {
    Serial.write(Serial3.read());
  }
}
