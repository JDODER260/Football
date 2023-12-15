/*************************************************************
  WARNING!
    It's very tricky to get it working. Please read this article:
    http://help.blynk.cc/hardware-and-libraries/arduino/esp8266-with-at-firmware

  This example shows how value can be pushed from Arduino to
  the Blynk App.

  NOTE:
  BlynkTimer provides SimpleTimer functionality:
    http://playground.arduino.cc/Code/SimpleTimer

  App dashboard setup:
    Value Display widget attached to Virtual Pin V5
 *************************************************************/

/* Fill-in information from Blynk Device Info here */
#define BLYNK_TEMPLATE_ID           "TMPL4gQcA9eZY"
#define BLYNK_TEMPLATE_NAME         "LED"
#define BLYNK_AUTH_TOKEN            "ZbglBKOmwioq__Ypu_h8cfImkHuWybJV"

/* Comment this out to disable prints and save space */
#define BLYNK_PRINT Serial

#include <ESP8266_Lib.h>
#include <BlynkSimpleShieldEsp8266.h>

// Your WiFi credentials.
// Set password to "" for open networks.
char ssid[] = "NtRuth";
char pass[] = "kilbrack087";

// Hardware Serial on Mega, Leonardo, Micro...
#define EspSerial Serial3

// or Software Serial on Uno, Nano...
//#include <SoftwareSerial.h>
//SoftwareSerial EspSerial(2, 3); // RX, TX

// Your ESP8266 baud rate:
#define ESP8266_BAUD 115200

ESP8266 wifi(&EspSerial);

BlynkTimer timer;

unsigned long previousMillis = 0;
const long interval = 1000; // Interval at which to send millis

void setup()
{
  // Debug console
  Serial.begin(115200);

  // Set ESP8266 baud rate
  EspSerial.begin(ESP8266_BAUD);
  delay(10);

  Blynk.begin(BLYNK_AUTH_TOKEN, wifi, ssid, pass);

  pinMode(2, OUTPUT); // Define pin 2 as an output for the LED

  Blynk.virtualWrite(V0, 0); // Initialize the LED state to off
}

// This function will be called every time the Virtual Pin V0 state changes
BLYNK_WRITE(V0) {
  int ledState = param.asInt(); // Get the state of the LED from the app

  digitalWrite(2, ledState); // Set the LED state according to the app

  if (ledState == HIGH) {
    Serial.println("LED is ON");
  } else {
    Serial.println("LED is OFF");
  }
}

void loop()
{
  Blynk.run();
  timer.run(); // Initiates BlynkTimer

  // Check if it's time to send millis
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    Blynk.virtualWrite(V5, millis() / 1000); // Send millis to Virtual Pin V5
  }
}
