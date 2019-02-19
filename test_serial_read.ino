/*
   Hello World!

   This is the Hello World! for Arduino.
   It shows how to send data to the computer
*/

String bearing_string = "";
int bearing_value = 0;

void setup()                    // run once, when the sketch starts
{
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);           // set up Serial library at 9600 bps
  delay(10000);
  Serial.println("get bearing");
}

void loop()                       // run over and over again
{
  if (Serial.available() > 0) {
    bearing_string = Serial.readStringUntil('\n'); // read the incoming byte:
    bearing_value = bearing_string.toInt();
  }

  if (bearing_value == 0) {
    digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
  }
  else if (bearing_value == 1111) {
    digitalWrite(LED_BUILTIN, LOW);    // turn the LED off by making the voltage LOW
  }
}
