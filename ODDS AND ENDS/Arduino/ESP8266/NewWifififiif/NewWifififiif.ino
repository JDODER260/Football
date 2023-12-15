#define BLYNK_TEMPLATE_ID "TMPL4gQcA9eZY"
#define BLYNK_TEMPLATE_NAME "LED"
#define BLYNK_AUTH_TOKEN "ZbglBKOmwioq__Ypu_h8cfImkHuWybJV"

#define BLYNK_PRINT Serial


#include <ESP8266_Lib.h>
#include <BlynkSimpleShieldEsp8266.h>


char ssid[] = "NtRuth";
char pass[] = "kilbrack087";

#define EspSerial Serial3


#define ESP8266_BAUD 115200

ESP8266 wifi(&EspSerial);

  BLYNK_WRITE(V0) {
  if (param.asInt()) {
    digitalWrite(2, HIGH);
    //turn led on arduino mega wifi
  }
  else {
    digitalWrite(2, LOW);
    //turn led off arduino mega wifi
  }

}

void setup()
{
  pinMode(2, OUTPUT);
  // Debug console
  Serial.begin(115200);

  // Set ESP8266 baud rate
  EspSerial.begin(ESP8266_BAUD);
  delay(10);

  Blynk.begin(BLYNK_AUTH_TOKEN, wifi, ssid, pass);
  // You can also specify server:
  //Blynk.begin(BLYNK_AUTH_TOKEN, wifi, ssid, pass, "blynk.cloud", 80);
  //Blynk.begin(BLYNK_AUTH_TOKEN, wifi, ssid, pass, IPAddress(192,168,1,100), 8080);
}

void loop()
{
  Blynk.run();

}
