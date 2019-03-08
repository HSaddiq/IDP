int analogPin = A3; // potentiometer wiper (middle terminal) connected to analog pin 3
                    // outside leads to ground and +5V
int val = 0;  // variable to store the value read

int divisions = 0;
float angle = 0;
bool colour;

void setup() {
  Serial.begin(9600);           //  setup serial
  val = analogRead(analogPin);  // read the input pin
  if (val <= 30) {
    colour = 0;
  }
  else {
    colour = 1;
  }
}

void loop() {
  val = analogRead(analogPin);  // read the input pin
  Serial.println(val);
  if ((val <= 5) && (colour == 1)) {
    colour = 0;
    divisions += 1;
    Serial.println(val);
  }
  else if ((val > 10) && (colour == 0)) {
    colour = 1;
    divisions += 1;
    Serial.println(angle);
  }

  angle = divisions * 3.6;
}
