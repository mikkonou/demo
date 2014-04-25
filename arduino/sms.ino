#include <SoftwareSerial.h>
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
SoftwareSerial mySerial(7, 8);

void myInit()
{
  String buffer = "";
  delay(200);
    
  mySerial.write("AT+CPIN?\r\r\n");
  delay(500);
  
  while (mySerial.available()) {
    buffer += (char)mySerial.read();
  }
  
  Serial.println(buffer);

  if (buffer.indexOf("SIM PIN") != -1)
  {
    Serial.println("PIN being sent...");
    mySerial.write("AT+CPIN=9505\r\r\n");
    delay(1000);
  } else {
    Serial.println("SIM already unlocked.");
  }
}

void displaySMS()
{
  String smsBuffer = "";
  String message = "";
  String msgSub;
  int firstIndex;
  int lastIndex;
  
  int i, j;
  int numberOfSubstrings;
  int row = 0;
  int substringStart;
  int substringEnd;
  
  mySerial.write("AT+CMGR=6\r\r\n");
  while(mySerial.available())
  {
    smsBuffer += (char)mySerial.read();
  }
  
  firstIndex = (smsBuffer.lastIndexOf("\"")) + 1;
  lastIndex = smsBuffer.lastIndexOf("\r\nOK\r\n");
  message = smsBuffer.substring(firstIndex, lastIndex);
  
  Serial.println(message);
  
  numberOfSubstrings = message.length() / 16;
  substringStart = 0;
  substringEnd = 15;
  
  lcd.clear();
  lcd.setCursor(0, 0);
  
  for (i=0; i <= message.length(); ++i)
  {
    lcd.setCursor(0, 0);
    
    if (substringEnd > message.length())
      substringEnd = message.length();
    
    msgSub = message.substring(substringStart, substringEnd);
    
    lcd.print(msgSub);
        
    substringStart++;
    substringEnd++;
    delay(200);
  }
}

void setup()
{
  mySerial.begin(19200);               // the GPRS baud rate   
  Serial.begin(19200);                 // the GPRS baud rate
  
  lcd.begin(16, 2);
  lcd.clear();
  
  myInit();
}

void loop()
{
  displaySMS();
  delay(3000);
}
