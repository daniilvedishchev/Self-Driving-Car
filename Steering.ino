const int ENA = 5;      // PWM for motor A
const int ENB = 6;      // PWM for motor B
const int IN1 = 8;      // Direction pin for motor A
const int IN2 = 9;      // Direction pin for motor A
const int IN3 = 10;     // Direction pin for motor B
const int IN4 = 11;     // Direction pin for motor B

// Define the pins for ultrasonic sensor
const int TRIG_PIN = 13;
const int ECHO_PIN = 12;


long duration;
int distance;

String CommunicationProtocol(){

  String receivedString = "";

  if (Serial.available() > 0) {
    // Read characters from the serial buffer until a newline is encountered
    while (Serial.available() > 0) {
      receivedString = Serial.readStringUntil('\n');  // Read one 
    }

    // Print the received string to the Serial Monitor
    Serial.println(receivedString);
  }
  return receivedString;
}

void AutomatedDriving(){

  String direction = CommunicationProtocol();

  if (direction != "Centered"){
    while (direction == "Left"){
      left(20);
      delay(300);
      direction = CommunicationProtocol();
    }
    while (direction == "Right"){
      right(20);
      delay(300);
      direction = CommunicationProtocol();
    }
  }
  left(0);
  right(0);

}

// Function to move the car forward with a specific speed
void forward(int motorSpeed) {
    // Set the direction pins for both motors to move forward
    digitalWrite(IN1, HIGH);   // Motor A forward
    digitalWrite(IN2, LOW);    // Motor A forward

    // Set PWM values for both motors to control their speed
    analogWrite(ENA, motorSpeed);  // Adjust motor A speed
}

void backward(int motorSpeed) {
    // Set the direction pins for both motors to move forward
    digitalWrite(IN1, LOW);   // Motor A forward
    digitalWrite(IN2, HIGH);    // Motor A forward

    // Set PWM values for both motors to control their speed
    analogWrite(ENA, motorSpeed);  // Adjust motor A speed
}
void right(int angle) {

  float ratio = 255/20;
  analogWrite(ENB, int(ratio*angle));

  digitalWrite(IN3, HIGH);   // Motor A forward
  digitalWrite(IN4, LOW);

}

void left(int angle) {

  float ratio = 255/20;
  analogWrite(ENB, int(ratio*angle));

  digitalWrite(IN3, LOW);   // Motor A forward
  digitalWrite(IN4, HIGH);

}


int mesure_distance(int trigPIN, int echoPIN){
    
    digitalWrite(trigPIN, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPIN, LOW);

    duration = pulseIn(echoPIN, HIGH);
    distance = duration * 0.0344 / 2;

    if (distance<500)
    {
      return distance;
    }
}

void setup() {
    Serial.begin(9600);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
}

void loop() {
  AutomatedDriving();
}

