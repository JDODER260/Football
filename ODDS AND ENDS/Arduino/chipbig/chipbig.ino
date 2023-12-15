int DataPin = 2;  // Data Pin is connected to Pin No. 2
int ClockPin = 3; // Data Pin is connected to Pin No. 3
int LatchPin = 4; // Data Pin is connected to Pin No. 4
byte Data = 0;  // 6 Bit Data to be sent through DataPin
// by www.andprof.com
void setup()
{
  Serial.begin(9600);
  pinMode(DataPin, OUTPUT);   // All 3 pins are output
  pinMode(ClockPin, OUTPUT);  
  pinMode(LatchPin, OUTPUT);
}


void loop()
{
  
  increment(); // LEDs increment start from 0 - 5   
  //delay(1000);  
  //SOS(); 
  //delay(1000);// All LEDs ON and OFF 10 times
  //OneByOne();   // LEDs Glow one by one from 0 to 5
  delay(1000);
  

}

// Function defined below

void shiftWrite(int Pin, boolean State) // Function is similar to digitalWrite 
{                                       // State-0/1 | Pin - Pin No.
  bitWrite(Data,Pin,State);             // Making Pin(Bit) 0 or 1
  shiftOut(DataPin, ClockPin, MSBFIRST, Data); // Data out at DataPin
  digitalWrite(LatchPin, HIGH);                // Latching Data
  digitalWrite(LatchPin, LOW);
}

void increment()   //LEDs increment start from 0 - 5 
{
  int PinNo = 0;
  int Delay = 200; 
  
  for(PinNo = 0; PinNo < 8; PinNo++)
  {
    shiftWrite(PinNo, HIGH);
    delay(Delay);                
  }
  for(PinNo = 7; PinNo >= 0; PinNo--)
  {
    shiftWrite(PinNo, LOW);
    delay(Delay);                
  }
}

void OneByOne()
{
  int DelayTime = 200;

  // Clear all LEDs
  for (int l = 0; l < 8; l++) {
    shiftWrite(l, LOW);
  }

  // Illuminate the third LED (LED 2)
  shiftWrite(2, HIGH);
  delay(DelayTime);
  shiftWrite(2, LOW);
}




void AllHigh()   // sets all High
{
  int PinNo = 0;
  for(PinNo = 0; PinNo < 8; PinNo++)
  {
   shiftWrite(PinNo, HIGH);  
  }
}

void AllLow()   // Sets all low
{
  int PinNo = 0;
  for(PinNo = 0; PinNo < 8; PinNo++)
  {
   shiftWrite(PinNo, LOW);  
  }
}

void SOS(){                  // All LEDs ON and OFF 10 times
  for (int x=0; x<2; x++){    
  AllHigh();
  delay(200);
  AllLow();
  delay(200);
  AllHigh();
  delay(200);
  AllLow();
  delay(200);
  AllHigh();
  delay(200);
  AllLow();
  delay(1000);
  AllHigh();
  delay(500);
  AllLow();
  delay(500);
  AllHigh();
  delay(500);
  AllLow();
  delay(500);
  AllHigh();
  delay(500);
  AllLow();
  delay(1000);
  AllHigh();
  delay(200);
  AllLow();
  delay(200);
  AllHigh();
  delay(200);
  AllLow();
  delay(200);
  AllHigh();
  delay(200);
  AllLow();
  delay(1000);
  }
}
