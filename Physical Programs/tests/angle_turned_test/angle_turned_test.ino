#include <Ultrasonic.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <motor.h>

using namespace std;

  String bearing_string = "";
  int bearing_value = 0;
  int current_bearing = 0;
  int direction = 0;

void setup() {
  Movement mov;
  //mov.get_threshold();
}

void rotate(int direction, int bearing){
  Movement mov;
  mov.turn(direction, 200, bearing);
}

void loop(){
    Serial.println("arduino ready");
    delay(500);
    if(Serial.readStringUntil('\n').equals("python ready"))
    {
      Serial.println("requesting bearing");
      delay(3000);

      //read bearing as a string and convert to integer
      bearing_string = Serial.readStringUntil('\n');
      bearing_value = bearing_string.toInt();

      //check if the bearing sent is valid and different to the previous one (to make sure it has been updated)
      if(bearing_value > 0 && bearing_value <= 360 && bearing_value != current_bearing)
      {
        Serial.println("received");
        current_bearing = bearing_value;

        //determines the direction of the turn based on the angle given
        if (bearing_value < 180) 
        {
          direction = 1; //LEFT
        }
        else
        {
          direction = 0; // RIGHT
          bearing_value = 360 - bearing_value;
        }

        //calls the rotate function with the given variables
        rotate(direction, bearing_value);
    }
}
}
