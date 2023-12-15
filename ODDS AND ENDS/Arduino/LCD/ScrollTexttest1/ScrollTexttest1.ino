#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);
String static_message = "I2C LCD Tut";
String scrolling_message = "Welcome to Microcontrollerslab! This is a scrolling message.";

void setup() { lcd.init(); lcd.backlight(); }

void loop() {
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
}
