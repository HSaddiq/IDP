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
bool ledge_procedure;
bool final_procedure;

String distance_string;
int distance_value;

int infra_pin;
int infra_val;

int LED_flash_pin;

unsigned long startMillis;
unsigned long currentMillis;
bool timeout_correction;


/***********************************************************************************************************************************/
//for direction, 0 is right (clockwise) 1 is left (anticlockwise)
void turn(int direction, int bearing){
  Movement mov;
  mov.turn(direction, 120, bearing);
}

/***********************************************************************************************************************************/
//1 for continuous, 0 for given distance
void drive(bool continuous, int direction = 0, int speed = 200, int distance = 0) {
  Movement mov;
  
  bool sensor_tripped = false;

  //if the drive mode is continuous, it will stop only when the infrared is tripped
  if(continuous){

    timeout_correction = false;
    startMillis = millis();
    
    mov.continuous_drive(speed);

    currentMillis = millis();
    
    while(!sensor_tripped && !timeout_correction){
      
      digitalWrite(LED_flash_pin, HIGH);
      infra_val = analogRead(infra_pin);

      currentMillis = millis();

      // if the continuous drive has been driving for more than 15 seconds, we assume something has gone wrong
      // so stop and request bearing to the next box
      if(currentMillis - startMillis > 18000 && !timeout_correction){
        timeout_correction = true;
        mov.drive(1, 200, 40);
        Serial.println("processed box");
      }
      
      if(infra_val > 100){
        sensor_tripped = true;
                
        mov.brake();
    
        mov.process_box();

        Serial.println("processed box");
      }
      
    }
    
  } 
  else
  {
    mov.drive(direction, speed, distance);
  }
}

/***********************************************************************************************************************************/
//A series of specific instructions for collecting the predictably located boxes
void initial_sweep(){
  
  Serial.println("starting initial sweep"); 
  
  drive(0, 0, 200, 210);
  drive(0, 1, 200, 15);
  turn(0, 105);
  drive(0, 1, 200, 40);

  //this checks if the robot is close enough to the wall every 30cm and makes small angle adjustments accordingly
  for(int i = 0; i < 6; i++){
    drive(0, 0, 200, 30);
    ultra_distance = ultrasonic.read(CM);

    if(ultra_distance >= 4){
      turn(1, 6);
    }
  }
  
  drive(0, 0, 200, 50);

  
  drive(0, 1, 200, 20 );
  turn(1, 90);
  drive(0, 0, 200, 30);
  drive(0, 1, 200, 30);
  turn(0, 179);
  
  drive(0, 1, 200, 35);
  drive(0, 0, 200, 130);

  /*turn(1, 90);
  drive(0, 0, 200, 30);
  drive(0, 1, 200, 30);
  turn(1, 179);
  
  drive(0, 0, 200, 50);*/

  turn(1,90);
  drive(0, 1, 200, 120);

  Serial.println("finished initial sweep");
}

/***********************************************************************************************************************************/
void empty_tray(){
  Movement mov;
  mov.dump_blocks();
}

/***********************************************************************************************************************************/
//defines initial state of variables and initiates the initial sweep
void setup() {
  Serial.begin(9600);
  bearing_string = "";
  bearing_value = 0;
  current_bearing = 0;
  direction = 0;

  ledge_procedure = true;
  final_procedure = false ;
  distance_string = "";
  distance_value = 0;

  infra_pin = A0;
  infra_val = 0;

  LED_flash_pin = 5;
  pinMode(LED_flash_pin, OUTPUT);

  initial_sweep();

}

/***********************************************************************************************************************************/
//main loop of programme, requesting bearing from the python
void loop(){
  Serial.println("requesting bearing");

  //read bearing as a string and convert to integer
  bearing_string = Serial.readStringUntil('\n');
  bearing_value = bearing_string.toInt();

  //if the bearing is 5000, this is the signal from Python that there are no more boxes, so we enter final procedure
  if(bearing_value == 5000){
    ledge_procedure = true;
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
    if(ledge_procedure){


      drive(0, 0, 200, 200);
      drive(0, 1, 150, 12);
      turn(0,94);
      
      empty_tray();

      if(final_procedure)
      {
        // drive forwards until the robot has straightened against the side of the table near the finish
        drive(0, 0, 200, 120);

        // reverse back into the finish box
        drive(0, 1, 200, 15);
      }
      else
      {
        turn(1, 15);
        drive(0, 1, 200, 200);
        drive(0, 0, 200, 30);
        turn(0, 90);
        drive(0, 0, 200, 50);
      }
      
      ledge_procedure = false;
      final_procedure = false;
    }
    //otherwise just drive until the infrared sensor is tripped
    else{
       drive(1);
    }
  }
}
