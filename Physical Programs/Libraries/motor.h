#ifndef Morse_h
#define Morse_h
#include <Wire.h>
#include <Adafruit_MotorShield.h>

using namespace std;
class Movement
{
  public:
  // Create the motor shield object with the default I2C address
  Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x60); 
  // Or, create it with a different I2C address (say for stacking)
  // Select which 'port' M1, M2, M3 or M4. In this case, M1
  Adafruit_DCMotor *myMotor1 = AFMS.getMotor(1);
  Adafruit_DCMotor *myMotor2 = AFMS.getMotor(2);
  int analogPin = A3; // potentiometer wiper (middle terminal) connected to analog pin 3
  int val = 0;  // variable to store the value read
  int divisions;
  bool colour;

  int lower_bound_for_high = 50;
  int upper_bound_for_low = 30;

  //Default constructor for setting up the motors in instantiation of object
  Movement()
  {
    Serial.begin(9600);           // set up Serial library at 9600 bps
    //Serial.println("Setting up movement...");

    AFMS.begin();  // create with the default frequency 1.6KHz
    val = analogRead(analogPin);  // read the input pin

    // Read the initial colour and record
    // (Throughout, 0 for black and 1 for white)
    if (val <= upper_bound_for_low) {
      colour = 0;
    }
    else {
      colour = 1;
    }
  }

  //If the physical setup of the robot changes, run get_threshold to calculate new bounds
  //for the encoder thresholding. This can either automatically update the values, or a print-out can
  //be viewed and the boundaries changed at the discretion of the user
  
  void get_threshold()
  {
    int sensor_reading;
    int largest = 0;
    int smallest = 1000;

    //Serial.println(sizeof(sensor_readings));
    myMotor1->setSpeed(200);
    myMotor1->run(BACKWARD);
    for(int i = 0; i < (500); i++)
    {
      sensor_reading = analogRead(analogPin);
      //Serial.println(sensor_reading);
      largest = (sensor_reading > largest) ? sensor_reading : largest;
      smallest = (sensor_reading < smallest) ? sensor_reading : smallest;
      
    }
    myMotor1->run(RELEASE);

    //prints the largest value read in the test
    Serial.print("largest...");
    Serial.println(largest);

    //prints the smallest value read in the test
    Serial.print("smallest...");
    Serial.println(smallest);

    lower_bound_for_high = largest - 25;
    upper_bound_for_low = smallest + 15;

  }

  //angle_div() will read the angle travelled by the wheel.  Returns number of divisions travelled
  //Used in drive and turn
  int angle_div()
  {
    val = analogRead(analogPin);  // read the input pin
    Serial.println(val);
    if ((val <= upper_bound_for_low) && (colour == 1)) 
    {
      colour = 0;
      divisions += 1;
    }
    else if ((val > lower_bound_for_high) && (colour == 0)) 
    {
      colour = 1;
      divisions += 1;
    }   
    return divisions;
  }
  
  //drive will move the robot forwards or backwards with a chosen direction (0 - backwards, 1 - forwards),
  //at a certain speed (lvl which ranges from 0 to 255) and for a certain duration (dur in seconds).
  void drive(bool dir, int lvl, float distance)
  {
    myMotor1->setSpeed(lvl);
    myMotor2->setSpeed(lvl);
    int divisions2 = round((50*distance)/(3.1416*5));
    Serial.println(divisions2);
    if(dir==0)
    {
      divisions = 0;
      Serial.println("Moving backwards...");
      while (angle_div()+3 < divisions2)
      {
        myMotor1->run(BACKWARD);
        myMotor2->run(BACKWARD);
      }
      Serial.println("Braking...");
      myMotor1->run(FORWARD);
      myMotor2->run(FORWARD);
      delay(20);
      myMotor1->run(RELEASE);
      myMotor2->run(RELEASE);
    }
    else
    {
      divisions = 0;
      Serial.println("Moving forwards...");
      while (angle_div()+3 < divisions2)
      {
        //Serial.println(angle_div());
        myMotor1->run(FORWARD);
        myMotor2->run(FORWARD);
      }
      Serial.println("Braking...");
      myMotor1->run(BACKWARD);
      myMotor2->run(BACKWARD);
      delay(20);
      myMotor1->run(RELEASE);
      myMotor2->run(RELEASE);
      goto end_drive;
    }
    end_drive:
        Serial.println("end driving...");
  }

  //turn() will rotate the robot on the spot a specified angle (in degrees)
  //at a certain level (lvl is an int between 0-255)
  //in a certain direction (dir is 0 for right and 1 for left)
  void turn(bool dir, int lvl, float angle)
  {
    float r = 14;
    myMotor1->setSpeed(lvl);
    myMotor2->setSpeed(lvl);
    int divisions2 = round((10*r*angle)/(36*5));
    
    if (dir==0)
    {
      divisions = 0;
      Serial.print("turning right...");
      Serial.print(angle);
      //Serial.println();
      
      while (angle_div() < divisions2)
      {
        myMotor1->run(FORWARD);
        myMotor2->run(BACKWARD);
      }
      Serial.println("Braking...");
      myMotor1->run(BACKWARD);
      myMotor2->run(FORWARD);
      delay(30);
      myMotor1->run(RELEASE);
      myMotor2->run(RELEASE);
      goto end_turn;
    }
     else
     {
      divisions = 0;
      Serial.print("turning left...");
      Serial.print(angle);
      //Serial.println();

      //can add constant here if it is overturning eg angle_div() +3
      while (angle_div() < divisions2)
      {
        myMotor1->run(BACKWARD);
        myMotor2->run(FORWARD);
      }
      Serial.println("Braking...");
      myMotor1->run(FORWARD);
      myMotor2->run(BACKWARD);
      delay(30);
      myMotor1->run(RELEASE);
      myMotor2->run(RELEASE);
      goto end_turn;
     }
      end_turn:
        Serial.println("end turning...");
    }

  void continuous_drive(int lvl)
  {
    myMotor1->setSpeed(lvl);
    myMotor2->setSpeed(lvl);

    myMotor1->run(FORWARD);
    myMotor2->run(FORWARD);
    
  }

  //brake is used with conditioned_drive to stop the  robot when a conditon is met
  void brake()
  {
      myMotor1->run(BACKWARD);
      myMotor2->run(BACKWARD);
      delay(20);
      myMotor1->run(RELEASE);
      myMotor2->run(RELEASE);
  }
};
#endif


