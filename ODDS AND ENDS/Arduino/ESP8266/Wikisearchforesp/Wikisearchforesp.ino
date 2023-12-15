#include <ESP8266WiFi.h>

char ssid[] = "FORBLYNK";
char pass[] = "kilbrack087";

const String wikipediaGetRequest = "GET /wiki/Moose HTTP/1.1\r\nHost: en.wikipedia.org\r\nConnection: close\r\n\r\n";

void setup() {
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Fetch Wikipedia page and send to Mega
  WiFiClient client;
  if (client.connect("en.wikipedia.org", 80)) {
    client.print(wikipediaGetRequest);
    while (client.connected()) {
      while (client.available()) {
        Serial.write(client.read());
      }
    }
    client.stop();
  }
}

void loop() {
}
