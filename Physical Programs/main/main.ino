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
  int ultra_distance;

  //for final procedure
  bool final_procedure;
  String distance_string;
  int distance_value;
  
  int infra_pin;
  int infra_val;

/***********************************************************************************************************************************/
//for direction, 0 is right (clockwise) 1 is left (anticlockwise)
void turn(int direction, int bearing){
  Movement mov;
  mov.turn(direction, 150, bearing);
}

/***********************************************************************************************************************************/
//1 for continuous, 0 for given distance
void drive(bool continuous, int direction = 0, int speed = 200, int distance = 0) {
  Movement mov;
  
  bool sensor_tripped = false;

  //if the drive mode is continuous, it will stop only when the infrared is tripped
  if(continuous){
    mov.continuous_drive(speed);
    
    while(!sensor_tripped){
      infra_val = digitalRead(infra_pin);
      if(infra_val == 1){
        sensor_tripped = true;
        
        //prints message for Python so it knows not to go to that box again, as it has already been processed
        Serial.println("processed box");
      }
    }
    delay(500);
    mov.brake();
  } 
  else
  {
    mov.drive(direction, speed, distance);
  }
}

/***********************************************************************************************************************************/
//A series of specific instructions for collecting the predictably located boxes
void initial_sweep(){
  int sonic_read = 0;
  
  Serial.println("conducting initial sweep");
  
  drive(0, 0, 200, 180);
  turn(0, 92);

  //this checks if the robot is close enough to the wall every 30cm and makes small angle adjustments accordingly
  for(int i = 0; i < 5; i++){
    drive(0, 0, 200, 30);
    sonic_read = ultrasonic.read(CM);

    if(sonic_read > 5){
      turn(1, 3);
    }else
    if(sonic_read < 4){
      turn(0, 3);
    }
    
  }
  
  drive(0, 0, 200, 30);
  turn(1, 90);
  drive(0, 1, 200, 20);
  turn(0,179);
  drive(0, 0, 200, 80);
  turn(1,90);
  drive(0, 1, 200, 30);
  turn(0, 179);
     
}

/***********************************************************************************************************************************/
//defines initial state of variables and initiates the initial sweep
void setup() {
  Serial.begin(9600);
  bearing_string = "";
  bearing_value = 0;
  current_bearing = 0;
  direction = 0;

  final_procedure = false;
  distance_string = "";
  distance_value = 0;

  //infra_pin = 11;
  //pinMode(infra_pin, INPUT);

  infra_val = 0;
 
  //initial_sweep();
}

/***********************************************************************************************************************************/
//main loop of programme, requesting bearing from the python
void loop(){
  Serial.println("requesting bearing");
  //delay(3000);

  //read bearing as a string and convert to integer
  bearing_string = Serial.readStringUntil('\n');
  bearing_value = bearing_string.toInt();

  //if the bearing is 5000, Python is telling us there are no more boxes, so we enter final procedure
  if(bearing_value == 5000){
    final_procedure = true;
    Serial.println("receieved final");
    delay(50);
    bearing_string = Serial.readStringUntil('\n');
    bearing_value = bearing_string.toInt();
  }
  
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

    //calls the turn function with the given variables
    turn(direction, bearing_value);

    //if it is the final procedure then we are heading for the shelf and want to overrun the motors to square up
    //the speed is also set slightly lower to avoid damage ocurring during the deliberate crash
    if(final_procedure){
      drive(0, 0, 150, 250);
      drive(0, 1, 150, 12);
      turn(0,90);
      drive(0, 0, 200, 60);
      final_procedure = false;
    }
    //otherwise just drive until the infrared sensor is tripped
    else{
       drive(1);
    }
  }
}
