#include <Ultrasonic.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <motor.h>

using namespace std;

  //for turn
  String bearing_string;
  int bearing_value;
  int current_bearing;
  int direction;

  //for ultrasound
  Ultrasonic ultrasonic(12,13);
  int distance;
  int previous_distance;

void setup() {
  Serial.begin(9600);
  bearing_string = "";
  bearing_value = 0;
  current_bearing = 0;
  direction = 0;

  previous_distance = 10000;
}

void rotate(int direction, int bearing){
  Movement mov;
  mov.turn(direction, 150, bearing);
}

void drive() {
  Movement mov;
  
  bool sensor_tripped = false;

  mov.continuous_drive(200);
  
  while(!sensor_tripped){
    distance = ultrasonic.read(CM);
    if(distance < 10){
      sensor_tripped = true;
    }
  }
  mov.brake(); 
}

void loop(){
  Serial.println("requesting bearing");
  //delay(3000);

  //read bearing as a string and convert to integer
  bearing_string = Serial.readStringUntil('\n');
  bearing_value = bearing_string.toInt();

  //check if the bearing sent is valid and different to the previous one (to make sure it has been updated)
  if(bearing_value > 0 && bearing_value <= 360 && bearing_value != current_bearing)
  {
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

    drive();
  }
}
