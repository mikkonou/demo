#include <SoftwareSerial.h>
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
SoftwareSerial mySerial(7, 8);

String serialBuffer = "";
char charBuffer;

void myInit()
{
  String buffer = "";
  delay(2000);
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

void parseRing()
{
  String phoneCallBuffer = "";
  String subString = "";
  String phoneNumber = "";
  String name = "";
  int firstIndex;
  int lastIndex;
  
  delay(300);
  
  while (mySerial.available()) {
    phoneCallBuffer += (char)mySerial.read();
  }
  
  firstIndex = phoneCallBuffer.indexOf("\"");
  lastIndex = phoneCallBuffer.lastIndexOf("\"");
  
  subString = phoneCallBuffer.substring(++firstIndex, lastIndex);

  phoneNumber = subString.substring(0, subString.indexOf("\""));
  name = subString.substring(subString.lastIndexOf("\"") + 1);

  delay(500);

  if (phoneNumber == "0456304625")
  {
    lcd.setCursor(0, 0);
    lcd.print("Authorized");
    lcd.setCursor(0, 1);
    lcd.print(name);
  } else {
    lcd.setCursor(0, 0);
    lcd.print("Unauthorized");
  }
  
  serialBuffer = "";
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
  if (mySerial.available())
  {
    charBuffer = mySerial.read();
    Serial.write(charBuffer);
    serialBuffer += charBuffer;
    if (serialBuffer.indexOf("RING") != -1)
    {
      parseRing();
    }
    if (serialBuffer.indexOf("NO CARRIER") != -1)
    {
      lcd.clear();
    }
  }
  if (Serial.available())
    mySerial.write(Serial.read());
}
