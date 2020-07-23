#define enablePin 8

#define plainDirPin 5
#define plainStepPin 2

#define rockerDirPin 6                                                       
#define rockerStepPin 3
#define rockerLimitSwitch 15

#define tableDirPin 7
#define tableStepPin 4
#define tableLimitSwitch 14


#define rightLaser 9
#define leftLaser 8

//Test
#define delayTime 1000
//Production
//#define delayTime 1000

#define stepsPerRevolution 8


void setup() {

  //Enable   
  pinMode(enablePin, OUTPUT);
  digitalWrite(enablePin, LOW);
  
  //Setup Laser
  pinMode(rightLaser, OUTPUT);
  pinMode(leftLaser, OUTPUT);

  //Setup Plain Stepper
  pinMode(plainStepPin, OUTPUT);
  pinMode(plainDirPin, OUTPUT);

  //Setup Rocker Stepper
  pinMode(rockerStepPin, OUTPUT);
  pinMode(rockerDirPin, OUTPUT);

  //Setup Table Stepper
  pinMode(tableStepPin, OUTPUT);
  pinMode(tableDirPin, OUTPUT);

  //Setup Limit Switch
  pinMode(rockerLimitSwitch, INPUT);
  pinMode(tableLimitSwitch, INPUT);
  
  //digitalWrite(12, LOW);
  Serial.begin(9600);
}

void loop() {
  handleSerial();
}

void handleSerial() {
  int tableLimitSwitchState;
  int rockerLimitSwitchState;
  
  //
  while(Serial.available() > 0) {
    String serialData = Serial.readStringUntil('\n');

      tableLimitSwitchState = digitalRead(tableLimitSwitch);
      rockerLimitSwitchState = digitalRead(rockerLimitSwitch);

      if(rockerLimitSwitchState == LOW) {
        Serial.println("ES10");
      }
      else if(rockerLimitSwitchState == HIGH) {
        Serial.println("ES11");
      }
      
      if(tableLimitSwitchState == LOW) {
        Serial.println("ES20");
      }
      else if(tableLimitSwitchState == HIGH) {
        Serial.println("ES21");
      }

      Serial.println(serialData);
      if(serialData[0] == 'L' ){
        handleLaser(serialData);
      }
      else if (serialData.equals("S10")) {
        digitalWrite(plainDirPin, HIGH);
        oneStep(plainStepPin);
      }
      else if (serialData.equals("S11")) {
        digitalWrite(plainDirPin, LOW);
        oneStep(plainStepPin);
      }
      else if (serialData.equals("S20")) {
        digitalWrite(rockerDirPin, HIGH);
        oneStep(rockerStepPin);
      }
      else if (serialData.equals("S21")) {
        digitalWrite(rockerDirPin, LOW);
        oneStep(rockerStepPin);
      }
      else if (serialData.equals("S30")) {
        digitalWrite(tableDirPin, HIGH);
        oneStep(tableStepPin);
      }
      else if (serialData.equals("S31")) {
        digitalWrite(tableDirPin, LOW);
        oneStep(tableStepPin);
     }
     Serial.println("0");
  }
}

void handleLaser(String serialData){
      if(serialData.equals("L11")){
        digitalWrite(rightLaser, HIGH);
      }
      else if (serialData.equals("L10")) {
        digitalWrite(rightLaser, LOW);
      }
      else if (serialData.equals("L21")) {
        digitalWrite(leftLaser, HIGH);
      }
      else if (serialData.equals("L20")) {
        digitalWrite(leftLaser, LOW);
      }
}

void oneStep(int stepper) {
    for (int i = 0; i < stepsPerRevolution; i++) {
    digitalWrite(stepper, HIGH);
    delayMicroseconds(delayTime);
    digitalWrite(stepper, LOW);
    delayMicroseconds(delayTime);
  }
}
