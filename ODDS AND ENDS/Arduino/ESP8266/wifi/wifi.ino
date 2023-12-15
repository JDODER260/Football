
#define BLYNK_TEMPLATE_ID "TMPL4cef9OvYd"
#define BLYNK_TEMPLATE_NAME "LED"

#define BLYNK_AUTH_TOKEN            "6SbkaBePN6zXwkELFDWKZFIy8bYdvLoz"

 

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

 

// This function sends Arduino's up time every second to Virtual Pin (5).

// In the app, Widget's reading frequency should be set to PUSH. This means

// that you define how often to send data to Blynk App.

void myTimerEvent()

{

 // You can send any value at any time.

 // Please don't send more that 10 values per second.

 Blynk.virtualWrite(V5, millis() / 1000);

}

 

void setup()

{

 // Debug console

 Serial.begin(115200);

 

 // Set ESP8266 baud rate

  EspSerial.begin(ESP8266_BAUD);

 delay(10);

 

 Blynk.begin(BLYNK_AUTH_TOKEN, wifi, ssid, pass);

 // You can also specify server:

 //Blynk.begin(BLYNK_AUTH_TOKEN, wifi, ssid, pass, "blynk.cloud", 80);

 //Blynk.begin(BLYNK_AUTH_TOKEN, wifi, ssid, pass, IPAddress(192,168,1,100), 8080);

 

 // Setup a function to be called every second

  timer.setInterval(1000L, myTimerEvent);

}

 

void loop()

{

 Blynk.run();

  timer.run(); // Initiates BlynkTimer

}

 
