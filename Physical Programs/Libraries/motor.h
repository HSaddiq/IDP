#ifndef Morse_h
#define Morse_h
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <Servo.h>

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
  
  //Add servo for pusher
  Servo pusher;
  
  // Define flipper motors
  Adafruit_DCMotor *myMotor3 = AFMS.getMotor(3);
  Adafruit_DCMotor *myMotor4 = AFMS.getMotor(4);
  
  
  int analogPin = A3;  // potentiometer wiper (middle terminal) connected to analog pin 3
  int val = 0;  // variable to store the value read
  int divisions;
  bool colour;

  int lower_bound_for_high = 45;  //the minimum value mesaured by encoder to be considered a high reading
  int upper_bound_for_low = 35;  //the maximum value mesaured by encoder to be considered a low reading

  int infra_pin;
  int infra_val;

  int hall_1_pin;
  int hall_2_pin;
  int hall_1_val;
  int hall_2_val;
  
  int LED_flash_pin;
  
  bool sensor_tripped = false;
  
  //Default constructor for setting up the motors in instantiation of object
  Movement()
  {
    Serial.begin(9600);           // set up Serial library at 9600 bps
    Serial.println("Setting up movement...");

    AFMS.begin();  // create with the default frequency 1.6KHz
    val = analogRead(analogPin);  // read the input pin
	
	infra_pin = 11;
	pinMode(infra_pin, INPUT);
	infra_val = 0;

	hall_1_pin = 8;
	hall_2_pin = 9;
	pinMode(hall_1_pin, INPUT);
	pinMode(hall_2_pin, INPUT);
	hall_1_val = 0;
	hall_2_val = 0;
	
	LED_flash_pin = 5;
	pinMode(LED_flash_pin, OUTPUT);

    // Read the initial colour and record
    // (Throughout, 0 for black and 1 for white)
    if (val <= upper_bound_for_low) {
      colour = 0;
    }
    else {
      colour = 1;
    }
  }
  
/***********************************************************************************************************************************/
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

/***********************************************************************************************************************************/
  //angle_div() will read the angle travelled by the wheel.  Returns number of divisions travelled
  //Used in drive and turn
  int angle_div()
  {
    val = analogRead(analogPin);  // read the input pin
    //Serial.println(val);
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

/***********************************************************************************************************************************/  
  //drive will move the robot forwards or backwards with a chosen direction (0 - forwards, 1 - backwards),
  //at a certain speed (lvl which ranges from 0 to 255) and for a certain distance (CM).
  //system 'quirk' -> to move forwards, motor set BACKWARD
  
  void drive(bool dir, int lvl, float distance)
  {
			
    myMotor1->setSpeed(lvl);
    myMotor2->setSpeed(lvl);
    int divisions2 = round((50*distance)/(3.1416*5));
    Serial.println(divisions2);
    if(dir==0)
    {
      divisions = 0;
      Serial.println("Moving forwards...");
      while (angle_div()+3 < divisions2)
      {
		digitalWrite(LED_flash_pin, HIGH);
        myMotor1->run(BACKWARD);
        myMotor2->run(BACKWARD);
		
		infra_val = digitalRead(infra_pin);
		if(infra_val == 1 && !sensor_tripped){
			brake();
			process_box();
			
			//this should reduce how much further it needs to travel
			//as it has just moved 5cm extra forwards.
			divisions2 = divisions2 - round((50*5)/(3.1416*5));
			
			myMotor1->setSpeed(lvl);
			myMotor2->setSpeed(lvl);
		}
      }
	  
	  
      Serial.println("Braking...");
	  Serial.println(distance);
      myMotor1->run(FORWARD);
      myMotor2->run(FORWARD);
      delay(30);
      myMotor1->run(RELEASE);
      myMotor2->run(RELEASE);
    }
    else
    {
      divisions = 0;
      Serial.println("Moving backwards...");
      while (angle_div()+3 < divisions2)
      {
        digitalWrite(LED_flash_pin, HIGH);
        myMotor1->run(FORWARD);
        myMotor2->run(FORWARD);
      }
      Serial.println("Braking...");
	  Serial.println(distance);
      myMotor1->run(BACKWARD);
      myMotor2->run(BACKWARD);
      delay(30);
      myMotor1->run(RELEASE);
      myMotor2->run(RELEASE);
      goto end_drive;
    }
    end_drive:
        Serial.println("end driving...");
		digitalWrite(LED_flash_pin, LOW);
  }

/***********************************************************************************************************************************/
  //turn() will rotate the robot on the spot a specified angle (in degrees)
  //at a certain level (lvl is an int between 0-255)
  //in a certain direction (dir is 0 for right and 1 for left)
  void turn(bool dir, int lvl, float angle)
  {
    float r = 12.5;
	
    myMotor1->setSpeed(lvl);
    myMotor2->setSpeed(lvl);
    int divisions2 = round((10*r*angle)/(36*5));
    
    if (dir==0)
    {
      divisions = 0;
      Serial.print("turning right...");
      Serial.print(angle);
      Serial.println();
      
	  //can add constant here if it is overturning eg angle_div() +3
      while (angle_div()+2 < divisions2)
      {
		digitalWrite(LED_flash_pin, HIGH);
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
      Serial.println();

      //can add constant here if it is overturning eg angle_div() +3
      while (angle_div()+2 < divisions2)
      {
		digitalWrite(LED_flash_pin, HIGH);
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
		digitalWrite(LED_flash_pin, LOW);
    }
	
/***********************************************************************************************************************************/  
  //this tells motors to run continuously until it is given a further instruction (ie brake)
  //again follows the system 'quirk' -> to move forwards, motor set BACKWARD
  void continuous_drive(int lvl)
  {  
	  
	Serial.println("continuous drive");
    myMotor1->setSpeed(lvl);
    myMotor2->setSpeed(lvl);

    myMotor1->run(BACKWARD);
    myMotor2->run(BACKWARD);
    
  }
  
/***********************************************************************************************************************************/
  //brake is used with conditioned_drive to stop the  robot when a conditon is met
  void brake()
  {
	Serial.println("braking");
    myMotor1->run(FORWARD);
    myMotor2->run(FORWARD);
    delay(30);
    myMotor1->run(RELEASE);
    myMotor2->run(RELEASE);
	
	digitalWrite(LED_flash_pin, LOW);
  }
  
/***********************************************************************************************************************************/
  //called when the infrared sensor has been tripped, signalling there is a box under the hall effect
  void process_box(){
	  
	sensor_tripped = true;
	
	hall_1_val = digitalRead(8);
	hall_2_val = digitalRead(9);
	
	Serial.println("processing box...");

	/* //both the hall effect values have to be 1 to signify the box is magnetic
	if(hall_1_val == 1 || hall_2_val == 1){

	  Serial.println("magnetic... discard");
	  
	  drive(0,100, 10);

	}
	else
	{
	  Serial.println("non-magnetic... storing box");

	  //drive forward so the box lines up with the pusher
	  drive(0,100, 10);
	  delay(2000);
	  brake();

	  //activate pusher
	  
	} */
	
	drive(0,100, 10);
	delay(2000);
	
	sensor_tripped = false;
  }
/***********************************************************************************************************************************/
  //moves forward the small amount between the sensors and the pusher
  void drive_to_pusher(){
	  continuous_drive(100);
	  
	  delay(800);
	  
	  brake();
	  
	  delay(4000);
  }

/***********************************************************************************************************************************/
  // Pusher function to activate servo, pushing blocks into bin

  void activate_pusher()
  {
    pusher.attach(9);  // attaches the servo on pin 9 to the servo object
    //run tipper motors backward to ensure contact with table
    myMotor3->setSpeed(255);
    myMotor4->setSpeed(255);
    myMotor3->run(BACKWARD);
    myMotor4->run(BACKWARD);

    while (iteration <= 2) {
      for (pos = 0; pos <= 180; pos += 12) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15ms for the servo to reach the position
      }
      for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15ms for the servo to reach the position
      }
      iteration = iteration + 1;
    }
  }

/***********************************************************************************************************************************/
  //the motor movement for the tipper
  void dump_blocks()
  {
	  myMotor3->setSpeed(255);
	  myMotor4->setSpeed(255);
	  myMotor3->run(FORWARD);
	  myMotor4->run(FORWARD);
	  delay(2000);
	  myMotor3->run(RELEASE);
	  myMotor4->run(RELEASE);

    myMotor3->run(BACKWARD);
	  myMotor4->run(BACKWARD);
	  delay(2000);
	  myMotor3->run(RELEASE);
	  myMotor4->run(RELEASE);
  }

};
#endif


