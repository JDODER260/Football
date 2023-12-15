/*************************************************************
  WARNING!
    It's very tricky to get it working. Please read this article:
    http://help.blynk.cc/hardware-and-libraries/arduino/esp8266-with-at-firmware

  You can send/receive any data using WidgetTerminal object.

  App dashboard setup:
    Terminal widget attached to Virtual Pin V1
 *************************************************************/

/* Fill-in information from Blynk Device Info here */
#define BLYNK_TEMPLATE_ID           "TMPL4gQcA9eZY"
#define BLYNK_TEMPLATE_NAME         "LED"
#define BLYNK_AUTH_TOKEN            "ZbglBKOmwioq__Ypu_h8cfImkHuWybJV"
const int dotDelay = 200;  // Duration of a dot in milliseconds
const int dashDelay = 4 * dotDelay; 
int ledPin = 2;
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

// Attach virtual serial terminal to Virtual Pin V1
WidgetTerminal terminal(V1);

// You can send commands from Terminal to your hardware. Just use
// the same Virtual Pin as your Terminal Widget
BLYNK_WRITE(V1)
{

  // if you type "Marco" into Terminal Widget - it will respond: "Polo:"
  if (String("Marco") == param.asStr()) {
    terminal.println("You said: 'Marco'") ;
    terminal.println("I said: 'Polo'") ;
    convertAndBlink(param.asStr());
  } else {

    // Send it back
    terminal.print("You said:");
    terminal.write(param.getBuffer(), param.getLength());
    terminal.println();
    convertAndBlink(param.asStr());
  }

  // Ensure everything is sent
  terminal.flush();
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

  // Clear the terminal content
  terminal.clear();

  // This will print Blynk Software version to the Terminal Widget when
  // your hardware gets connected to Blynk Server
  terminal.println(F("Blynk v" BLYNK_VERSION ": Device started"));
  terminal.println(F("-------------"));
  terminal.println(F("Type 'Marco' and get a reply, or type"));
  terminal.println(F("anything else and get it printed back."));
  terminal.flush();
}

void loop()
{
  Blynk.run();
}


void convertAndBlink(String text) {
  for (int i = 0; i < text.length(); i++) {
    char character = text.charAt(i);
    switch (character) {
      case 'A': blink(".-"); break;
      case 'B': blink("-..."); break;
      case 'C': blink("-.-."); break;
      case 'D': blink("-.."); break;
      case 'E': blink("."); break;
      case 'F': blink("..-."); break;
      case 'G': blink("--."); break;
      case 'H': blink("...."); break;
      case 'I': blink(".."); break;
      case 'J': blink(".---"); break;
      case 'K': blink("-.-"); break;
      case 'L': blink(".-.."); break;
      case 'M': blink("--"); break;
      case 'N': blink("-."); break;
      case 'O': blink("---"); break;
      case 'P': blink(".--."); break;
      case 'Q': blink("--.-"); break;
      case 'R': blink(".-."); break;
      case 'S': blink("..."); break;
      case 'T': blink("-"); break;
      case 'U': blink("..-"); break;
      case 'V': blink("...-"); break;
      case 'W': blink(".--"); break;
      case 'X': blink("-..-"); break;
      case 'Y': blink("-.--"); break;
      case 'Z': blink("--.."); break;
      case ' ': delay(4 * dotDelay); break; // Space between words
      default: Serial.println("Invalid character: " + String(character)); break;
    }
    delay(dotDelay); // Space between characters
  }
}

void blink(String morse) {
  for (int i = 0; i < morse.length(); i++) {
    char signal = morse.charAt(i);
    if (signal == '.') {
      digitalWrite(ledPin, HIGH);
      delay(dotDelay);
      digitalWrite(ledPin, LOW);
    } else if (signal == '-') {
      digitalWrite(ledPin, HIGH);
      delay(dashDelay);
      digitalWrite(ledPin, LOW);
    }
    delay(dotDelay); // Space between signals within a character
  }
}
