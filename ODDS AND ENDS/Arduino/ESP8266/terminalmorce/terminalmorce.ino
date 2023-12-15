#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);
String static_message = "Blynk Try";
String scrolling_message = "";

/* Fill-in information from Blynk Device Info here */
#define BLYNK_TEMPLATE_ID           "TMPL4gQcA9eZY"
#define BLYNK_TEMPLATE_NAME         "LED"
#define BLYNK_AUTH_TOKEN            "ZbglBKOmwioq__Ypu_h8cfImkHuWybJV"
const int dotDelay = 100;  // Duration of a dot in milliseconds
const int dashDelay = 3 * dotDelay; 
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
  
  // Initialize the LCD
  lcd.init();
  lcd.backlight();
}

void loop()
{
  lcd.setCursor(0, 0);
  lcd.print(static_message);
  String scrolled = scrolling_message + " ";
  int msg_len = scrolled.length();

  for (int p = 0; p < msg_len; p++) {
    lcd.setCursor(0, 1);
    String display_msg = scrolled.substring(p, p + 16);

    if (p + 16 > msg_len) {
      display_msg += scrolled.substring(0, 16 - (msg_len - p));
    }

    lcd.print(display_msg);
    delay(250);
  }

  Blynk.run(); // Run Blynk

  // Your existing loop code...
}

void convertAndBlink(String text) {
  text = " " + text;
  scrolling_message = "";
  for (int i = 0; i < text.length(); i++) {
    char character = text.charAt(i);
    switch (character) {
      case 'A': case 'a': blink(".-", character); break;
      case 'B': case 'b': blink("-...", character); break;
      case 'C': case 'c': blink("-.-.", character); break;
      case 'D': case 'd': blink("-..", character); break;
      case 'E': case 'e': blink(".", character); break;
      case 'F': case 'f': blink("..-.", character); break;
      case 'G': case 'g': blink("--.", character); break;
      case 'H': case 'h': blink("....", character); break;
      case 'I': case 'i': blink("..", character); break;
      case 'J': case 'j': blink(".---", character); break;
      case 'K': case 'k': blink("-.-", character); break;
      case 'L': case 'l': blink(".-..", character); break;
      case 'M': case 'm': blink("--", character); break;
      case 'N': case 'n': blink("-.", character); break;
      case 'O': case 'o': blink("---", character); break;
      case 'P': case 'p': blink(".--.", character); break;
      case 'Q': case 'q': blink("--.-", character); break;
      case 'R': case 'r': blink(".-.", character); break;
      case 'S': case 's': blink("...", character); break;
      case 'T': case 't': blink("-", character); break;
      case 'U': case 'u': blink("..-", character); break;
      case 'V': case 'v': blink("...-", character); break;
      case 'W': case 'w': blink(".--", character); break;
      case 'X': case 'x': blink("-..-", character); break;
      case 'Y': case 'y': blink("-.--", character); break;
      case 'Z': case 'z': blink("--..", character); break;
      case '0': blink("-----", character); break; 
      case '1': blink(".----", character); break; 
      case '2': blink("..---", character); break; 
      case '3': blink("...--", character); break; 
      case '4': blink("....-", character); break; 
      case '5': blink(".....", character); break; 
      case '6': blink("-....", character); break; 
      case '7': blink("--...", character); break; 
      case '8': blink("---..", character); break; 
      case '9': blink("----.", character); break; 
      case ' ': delay(4 * dotDelay); scrolling_message = scrolling_message + character; LcdPrint(); break; // Space between words
      case '.': blink(".-.-.-", character); break; 
      case ',': blink("--..--", character); break; 
      case '?': blink("..--..", character); break; 
      case '\'': blink(".----.", character); break; 
      case '!': blink("-.-.--", character); break; 
      case '/': blink("-..-.", character); break; 
      case '(': blink("-.--.", character); break; 
      case ')': blink("-.--.-", character); break; 
      case '&': blink(".-...", character); break; 
      case ':': blink("---...", character); break; 
      case ';': blink("-.-.-.", character); break; 
      case '=': blink("-...-", character); break; 
      case '+': blink(".-.-.", character); break; 
      case '-': blink("-....-", character); break; 
      case '_': blink("..--.-", character); break; 
      case '"': blink(".-..-.", character); break; 
      case '$': blink("...-..-", character); break; 
      case '@': blink(".--.-.", character); break; 
      default: Serial.println("Invalid character: " + String(character)); break;
    }
    delay(100); // Space between characters
  }
}

void blink(String morse, char character) { // Added 'char character' parameter
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
    delay(100); // Space between signals within a character
  }
  scrolling_message = scrolling_message + character;
  LcdPrint();
}

void LcdPrint() {
  lcd.setCursor(0, 0);
  lcd.print(static_message);
  String scrolled = scrolling_message + " ";
  int msg_len = scrolled.length();

  for (int p = 0; p < msg_len; p++) {
    lcd.setCursor(0, 1);
    String display_msg = scrolled.substring(p, p + 16);

    if (p + 16 > msg_len) {
      display_msg += scrolled.substring(0, 16 - (msg_len - p));
    }

    lcd.print(display_msg);
    //delay(10);
  }
}

// Function to scroll terminal input
void scrollTerminalInput(String text) {
  scrolling_message += text; // Append the received text
  scrolling_message += " "; // Add space between messages
}
